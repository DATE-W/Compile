import os.path

from src.lexer import Lexer
from src.parser.Grammar import Grammar
from src.parser.LR1Table import LR1Table


class Codegen:
    class Code:
        def __init__(self, op, arg1=None, arg2=None, result=None, line=None):
            self.op = op
            self.arg1 = arg1
            self.arg2 = arg2
            self.result = result
            self.line = line

        def __str__(self):
            return (f'{self.line}: '
                    f'({self.op}, '
                    f'{self.arg1 if self.arg1 else "-"}, '
                    f'{self.arg2 if self.arg2 else "-"}, '
                    f'{self.result})')

        def write_back(self, result):
            self.result = result

    class SymbolTableItem:
        def __init__(self, name, type, value, defined, addr):
            self.name = name
            self.type = type
            self.value = value
            self.defined = defined
            self.addr = addr

        def __str__(self):
            return f'{self.name}\t{self.type}\t{self.value}\t{self.defined}\t{self.addr}'

    def __init__(self, reduce_list):
        self.reduce_list = reduce_list
        self.code: dict[int: Codegen.Code] = {}  # 用dict便于回填
        self.temp_counter = 0  # 记录当前临时变量
        self.line_counter = 100  # 当前行数
        self.stack = []
        self.var_dict = {}
        self.const_dict = {}
        self.while_stack = []  # 记录循环开始的行和需要回填的行
        self.if_stack = []  # 记录需要回填的行
        self.symbol_table = {}

    def __str__(self):
        res = ''
        for c in self.code:
            res += f'{self.code[c]}\n'
        return res

    def add_var(self, name: str):
        if name in self.var_dict or name in self.const_dict:
            raise RuntimeError(f'Redefinition in var {name}')
        self.var_dict[name] = ''

    def update_var(self, name: str, value: str):
        if name not in self.var_dict:
            if name in self.const_dict:
                raise RuntimeError(f'Cannot assign const {name}')
            else:
                raise RuntimeError(f'Undefined var {name}')
        self.var_dict[name] = value

    def add_const(self, name: str, value: str):
        if name in self.const_dict:
            raise RuntimeError(f'Redefinition in const {name}')
        self.const_dict[name] = value

    def get_value(self, name: str):
        if name in self.const_dict:
            return self.const_dict[name]
        else:
            if name in self.var_dict:
                return self.var_dict[name]
            else:
                raise RuntimeError(f'Undefined var {name}')

    def print_dict(self):
        print("const:")
        print(self.const_dict)
        print("var:")
        print(self.var_dict)

    def new_temp(self):
        temp_var = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_var

    def emit(self, op, result, arg1=None, arg2=None):
        self.code[self.line_counter] = self.Code(op, arg1, arg2, result, self.line_counter)
        # print(f'emit: {self.code[self.line_counter]}')
        self.line_counter += 1

    def process(self):
        for r in self.reduce_list:
            production = r[0]
            value = r[1]
            # print(f'\nProduction: {production}, value: {value}')

            if production == 'ID -> id' or production == 'UINT -> num':
                self.stack.append(value)

            elif production == 'ASSIGN_STATEMENT -> ID := EXPR':
                if len(self.stack) < 2:
                    raise RuntimeError(f"Stack underflow in production \'{production}\'")
                value = self.stack.pop()
                name = self.stack.pop()
                self.update_var(name, value)
                self.emit(':=', name, value)

            elif production == 'CONST_DEF -> ID = UINT':
                if len(self.stack) < 2:
                    raise RuntimeError(f"Stack underflow in production \'{production}\'")
                value = self.stack.pop()
                name = self.stack.pop()
                self.add_const(name, value)
                self.emit(':=', name, value)

            elif production.startswith('VARIABLE_ ->'):
                if len(self.stack) < 1:
                    raise RuntimeError(f"Stack underflow in production \'{production}\'")
                name = self.stack.pop()
                self.add_var(name)

            elif production == 'HEADER -> PROGRAM ID':
                if len(self.stack) < 1:
                    raise RuntimeError(f"Stack underflow in production \'{production}\'")
                self.stack.pop()

            elif production == 'COMP_STATEMENT -> COMP_BEGIN END' \
                    or production.startswith('COMP_BEGIN'):
                pass  # 暂时不用处理

            elif production.startswith('REL ->') \
                    or production.startswith('MUL ->') \
                    or production.startswith('PLUS ->'):
                op = production.split('-> ')[-1]
                self.stack.append(op)

            elif production == 'EXPR -> EXPR PLUS ITEM' \
                    or production == 'ITEM -> ITEM MUL FACTOR':
                if len(self.stack) < 3:
                    raise RuntimeError(f"Stack underflow in production \'{production}\'")
                right = self.stack.pop()
                op = self.stack.pop()
                left = self.stack.pop()
                temp = self.new_temp()
                self.stack.append(temp)
                self.emit(op, temp, left, right)

            elif production == 'EXPR -> PLUS ITEM':  # 正负号
                if len(self.stack) < 2:
                    raise RuntimeError(f"Stack underflow in production \'{production}\'")
                item = self.stack.pop()
                op = self.stack.pop()
                if op == '-':
                    temp = self.new_temp()
                    self.stack.append(temp)
                    self.emit('uminus', temp, item)
                else:
                    self.stack.append(item)

            elif production == 'CONDITION -> EXPR REL EXPR':
                if len(self.stack) < 3:
                    raise RuntimeError(f"Stack underflow in production \'{production}\'")
                right = self.stack.pop()
                op = self.stack.pop()
                left = self.stack.pop()
                self.emit(f'j{op}', self.line_counter + 2, left, right)  # 跳转至真出口，即下下句

            elif production == 'COND_STATEMENT -> IF CONDITION THEN M_IF STATEMENT':
                self.code[self.if_stack.pop()].write_back(self.line_counter)  # 回填

            elif production == 'WHILE_STATEMENT -> WHILE M_BEFORE_WHILE CONDITION DO M_AFTER_WHILE STATEMENT':
                write_back = self.while_stack.pop()
                jump_back = self.while_stack.pop()

                self.emit('j', jump_back)  # 先跳回循环判断
                self.code[write_back].write_back(self.line_counter)  # 再回填

            elif production == 'M_IF -> ^':
                self.if_stack.append(self.line_counter)  # 记录假出口所在行
                self.emit('j', -1)  # 假出口，等待回填

            elif production == 'M_BEFORE_WHILE -> ^':
                self.while_stack.append(self.line_counter)  # 记录循环开始的行

            elif production == 'M_AFTER_WHILE -> ^':
                self.while_stack.append(self.line_counter)  # 记录假出口所在行
                self.emit('j', -1)  # 假出口，等待回填

            # print(f'Stack: {self.stack}')
            # print(f'var_dict: {self.var_dict}')
            # print(f'const_dict: {self.const_dict}')
            # print(f'while_stack: {self.while_stack}')
            # print(f'if_stack: {self.if_stack}')
            # print(f'line: {self.line_counter}')
        self.print_dict()


if __name__ == '__main__':
    grammar = Grammar(open('../parser/grammars/grammar.pl0').read())
    path = '../in/test.pl0'
    with open(path, "r") as f:
        code = f.read()
    codegen = Codegen((LR1Table(grammar).
                       get_reduce_result(Lexer(code).tokenize())))
    try:
        codegen.process()
        print('\nCode: ')
        print(codegen)
        with open(f'./out/{os.path.basename(path).split(".")[0]}-out.txt', 'w') as file:
            file.write(str(codegen))
    except RuntimeError as re:
        print(re)
