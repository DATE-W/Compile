class Codegen:
    def __init__(self, reduce_result):
        self.reduce_result = reduce_result
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.stack = []

    def new_temp(self):
        temp_var = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_var

    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def emit(self, op, arg1, arg2=None, result=None, label=None):
        if label:
            line = f"{label}: "
        else:
            line = "    "

        if arg2 is None:
            line += f"{result} := {arg1}"
        else:
            line += f"if {arg1} {op} {arg2} goto {result}"
        self.code.append(line)

    def process(self):
        for generative, value in zip(self.reduce_result[::2], self.reduce_result[1::2]):
            if generative == 'ID -> id' or generative == 'UINT -> num':
                self.stack.append(value)

            elif generative == 'ASSIGN_STATEMENT -> ID := EXPR':
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow in ASSIGN_STATEMENT")
                expr = self.stack.pop()
                var = self.stack.pop()
                self.emit(':=', var, expr)

            elif generative == 'EXPR -> EXPR PLUS ITEM':
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow in EXPR -> EXPR PLUS ITEM")
                item = self.stack.pop()
                expr = self.stack.pop()
                temp = self.new_temp()
                self.emit('+', expr, item, temp)
                self.stack.append(temp)

            elif generative == 'ITEM -> ITEM MUL FACTOR':
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow in ITEM -> ITEM MUL FACTOR")
                factor = self.stack.pop()
                item = self.stack.pop()
                temp = self.new_temp()
                self.emit('*', item, factor, temp)
                self.stack.append(temp)

            elif generative == 'CONDITION -> EXPR REL EXPR':
                if len(self.stack) < 3:
                    raise RuntimeError("Stack underflow in CONDITION")
                right = self.stack.pop()
                rel = self.stack.pop()
                left = self.stack.pop()
                temp = self.new_temp()
                self.emit(rel, left, right, temp)
                self.stack.append(temp)

            elif generative == 'COND_STATEMENT -> IF CONDITION THEN STATEMENT':
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow in COND_STATEMENT")
                statement = self.stack.pop()
                condition = self.stack.pop()
                label_true = self.new_label()
                label_end = self.new_label()
                self.emit('if', condition, 'goto', label_true)
                self.emit('goto', label_end)
                self.code.append(f"{label_true}: {statement}")
                self.code.append(f"{label_end}:")

            elif generative == 'WHILE_STATEMENT -> WHILE CONDITION DO STATEMENT':
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow in WHILE_STATEMENT")
                statement = self.stack.pop()
                condition = self.stack.pop()
                label_start = self.new_label()
                label_end = self.new_label()
                self.code.append(f"{label_start}:")
                self.emit('if', condition, 'goto', label_end)
                self.code.append(statement)
                self.emit('goto', label_start)
                self.code.append(f"{label_end}:")

            # 其他必要的产生式处理...
            # 例如，处理常量和变量声明...

        return self.code


# Example reduce_result
reduce_result = [
    'ID -> id', 'test',
    'HEADER -> PROGRAM ID', '',
    'ID -> id', 'a',
    'UINT -> num', '1',
    'CONST_DEF -> ID = UINT', '',
    'CONST_ -> CONST CONST_DEF', '',
    'ID -> id', 'b',
    'UINT -> num', '2',
    'CONST_DEF -> ID = UINT', '',
    'CONST_ -> CONST_ , CONST_DEF', '',
    'CONST_STATEMENT -> CONST_ ;', '',
    'ID -> id', 'x',
    'VARIABLE_ -> VAR ID', '',
    'ID -> id', 'y',
    'VARIABLE_ -> VARIABLE_ , ID', '',
    'VARIABLE_STATEMENT -> VARIABLE_ ;', '',
    'ID -> id', 'x',
    'UINT -> num', '1',
    'FACTOR -> UINT', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'ASSIGN_STATEMENT -> ID := EXPR', '',
    'STATEMENT -> ASSIGN_STATEMENT', '',
    'COMP_BEGIN -> BEGIN STATEMENT', '',
    'ID -> id', 'y',
    'UINT -> num', '2',
    'FACTOR -> UINT', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'ASSIGN_STATEMENT -> ID := EXPR', '',
    'STATEMENT -> ASSIGN_STATEMENT', '',
    'COMP_BEGIN -> COMP_BEGIN ; STATEMENT', '',
    'ID -> id', 'x',
    'FACTOR -> ID', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'REL -> <', '',
    'ID -> id', 'y',
    'FACTOR -> ID', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'CONDITION -> EXPR REL EXPR', '',
    'ID -> id', 'x',
    'UINT -> num', '3',
    'FACTOR -> UINT', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'ASSIGN_STATEMENT -> ID := EXPR', '',
    'STATEMENT -> ASSIGN_STATEMENT', '',
    'COMP_BEGIN -> BEGIN STATEMENT', '',
    'ID -> id', 'x',
    'FACTOR -> ID', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'REL -> >', '',
    'ID -> id', 'y',
    'FACTOR -> ID', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'CONDITION -> EXPR REL EXPR', '',
    'ID -> id', 'y',
    'UINT -> num', '4',
    'FACTOR -> UINT', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'ASSIGN_STATEMENT -> ID := EXPR', '',
    'STATEMENT -> ASSIGN_STATEMENT', '',
    'COND_STATEMENT -> IF CONDITION THEN STATEMENT', '',
    'STATEMENT -> COND_STATEMENT', '',
    'COMP_BEGIN -> COMP_BEGIN ; STATEMENT', '',
    'COMP_STATEMENT -> COMP_BEGIN END', '',
    'STATEMENT -> COMP_STATEMENT', '',
    'COND_STATEMENT -> IF CONDITION THEN STATEMENT', '',
    'STATEMENT -> COND_STATEMENT', '',
    'COMP_BEGIN -> COMP_BEGIN ; STATEMENT', '',
    'ID -> id', 'x',
    'FACTOR -> ID', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'REL -> <', '',
    'UINT -> num', '6',
    'FACTOR -> UINT', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'CONDITION -> EXPR REL EXPR', '',
    'ID -> id', 'x',
    'ID -> id', 'y',
    'FACTOR -> ID', '',
    'ITEM -> FACTOR', '',
    'EXPR -> ITEM', '',
    'PLUS -> +', '',
    'UINT -> num', '1',
    'FACTOR -> UINT', '',
    'ITEM -> FACTOR', '',
    'EXPR -> EXPR PLUS ITEM', '',
    'ASSIGN_STATEMENT -> ID := EXPR', '',
    'STATEMENT -> ASSIGN_STATEMENT', '',
    'COMP_BEGIN -> BEGIN STATEMENT', '',
    'ID -> id', 'y',
    'ID -> id', 'y',
    'FACTOR -> ID', '',
    'ITEM -> FACTOR', '',
    'MUL -> *', '',
    'ID -> id', 'x',
    'FACTOR -> ID', '',
    'ITEM -> ITEM MUL FACTOR', '',
    'EXPR -> ITEM', '',
    'ASSIGN_STATEMENT -> ID := EXPR', '',
    'STATEMENT -> ASSIGN_STATEMENT', '',
    'COMP_BEGIN -> COMP_BEGIN ; STATEMENT', '',
    'COMP_STATEMENT -> COMP_BEGIN END', '',
    'STATEMENT -> COMP_STATEMENT', '',
    'WHILE_STATEMENT -> WHILE CONDITION DO STATEMENT', '',
    'STATEMENT -> WHILE_STATEMENT', '',
    'COMP_BEGIN -> COMP_BEGIN ; STATEMENT', '',
    'COMP_STATEMENT -> COMP_BEGIN END', '',
    'STATEMENT -> COMP_STATEMENT', '',
    'SUBPROG -> CONST_STATEMENT VARIABLE_STATEMENT STATEMENT', '',
    'PROG -> HEADER SUBPROG', ''
]

codegen = Codegen(reduce_result)
try:
    tac = codegen.process()
    for line in tac:
        print(line)
except RuntimeError as e:
    print(f"Error during code generation: {e}")
