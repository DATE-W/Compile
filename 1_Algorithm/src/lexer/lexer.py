import re
from collections import namedtuple

# 定义 Token 数据结构，包含类型、值、行号和列号
# Token = namedtuple('Token', ['type', 'keyword', 'value', 'line', 'column'])
Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

class Lexer:
    @staticmethod
    def get_code(filepath):
        with open(filepath, 'r') as file:
            ret = ''
            for line in file:
                ret += line.strip()
        return ret

    # 需要参数为文件路径
    def __init__(self, code):
        # self.code = self.get_code(filepath)  # 源代码字符串
        self.code = code
        self.tokens = []  # 存储生成的 tokens
        self.current_line = 1  # 当前行号
        self.current_column = 1  # 当前列号

        # PL/0 词法规则定义
        self.token_specification = {
            'PROGRAM': r'PROGRAM',  # 程序开始关键字
            'BEGIN': r'BEGIN',  # 开始关键字
            'END': r'END',  # 结束关键字
            'CONST': r'CONST',  # 常量声明关键字
            'VAR': r'VAR',  # 变量声明关键字
            'WHILE': r'WHILE',  # 循环关键字
            'DO': r'DO',  # 执行关键字
            'IF': r'IF',  # 条件判断关键字
            'THEN': r'THEN',  # 条件成立时执行关键字
            'num': r'\d+',  # 整数
            'id': r'[a-z][a-z0-9]*',  # 标识符
            'ASSIGN': r':=',  # 赋值运算符
            'NE': r'<>',  # 不等于运算符
            'LE': r'<=',  # 小于等于运算符
            'GE': r'>=',  # 大于等于运算符
            'EQ': r'=',  # 判等运算符
            'GR': r'>',  # 小于运算符
            'LS': r'<',  # 大于运算符
            # 'OP': r'[+-*/]',
            'ADD': r'\+',    # 加法运算符
            'SUB': r'\-',    # 减法运算符
            'MUL': r'\*',    # 乘法运算符
            'DIV': r'/',    # 除法运算符
            'LBRACKET': r'\(',  # 左括号
            'RBRACKET': r'\)',  # 右括号
            'SEMICOLON': r';',  # 分号
            'COMMA': r',',  # 逗号
            'NEWLINE': r'\n',  # 新行
            'SKIP': r'[ \t]+',  # 跳过空格和制表符
            'MISMATCH': r'.',  # 任何其他字符
        }

    @staticmethod
    def generate_token(self, match):
        token_type = match.lastgroup
        if token_type == 'NEWLINE':
            # 更新行号和列号
            self.current_line += 1
            self.current_column = 0
        elif token_type != 'SKIP':
            # 生成并添加 token
            # value = match.group(token_type)
            # keyword = self.token_specification[token_type] if token_type not in ['ID', 'NUMBER'] else ('id' if token_type == 'ID' else 'num')
            # if token_type in ['ADD', 'SUB', 'MUL', 'DIV']:
            #     keyword = value
            # token = Token(token_type, keyword, value, self.current_line, self.current_column)
            # self.tokens.append(token)
            value = match.group(token_type)
            if token_type == 'END':
                print('1\n')
            if token_type not in ['id', 'num']:
                token_type = value
                value = ''

            token = Token(token_type, value, self.current_line, self.current_column)
            self.tokens.append(token)
        self.current_column += match.end() - match.start()

    def tokenize(self):
        # 创建正则表达式并编译
        tok_regex = '|'.join('(?P<%s>%s)' % (key, val) for key, val in self.token_specification.items())
        get_token = re.compile(tok_regex).match
        pos = 0
        # 逐字符遍历源代码
        while pos < len(self.code):
            match = get_token(self.code, pos)
            if match is not None:
                self.generate_token(self, match)
                pos = match.end()
            else:
                # 处理无法匹配的字符
                raise RuntimeError(
                    f'Unexpected character {self.code[pos]} at line {self.current_line} column {self.current_column}')
        for t in self.tokens:
            print(t)
        return self.tokens


# 示例使用
if __name__ == "__main__":
    path = './test2.txt'
    # code = '''
    # PROGRAM example;
    # VAR x, y;
    # BEGIN
    #     x := 2;
    #     IF x > 3 THEN
    #         y := x + 5;
    #     END;
    # '''
    with open(path, "r") as f:
        code = f.read()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    with open('./token2.txt', 'w') as file:
        for token in tokens:
            file.write('\'{a}\', \'{b}\', {c}, {d}\n'.format(a=token.type, b=token.value, c=token.line, d=token.column))
