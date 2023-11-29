import re
from collections import namedtuple

# 定义 Token 数据结构，包含类型、值、行号和列号
Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

class Lexer:
    def __init__(self, code):
        self.code = code          # 源代码字符串
        self.tokens = []          # 存储生成的 tokens
        self.current_line = 1     # 当前行号
        self.current_column = 1   # 当前列号

        # PL/0 词法规则定义
        self.token_specification = [
            ('PROGRAM', r'PROGRAM'),  # 程序开始关键字
            ('BEGIN',   r'BEGIN'),    # 开始关键字
            ('END',     r'END'),      # 结束关键字
            ('CONST',   r'CONST'),    # 常量声明关键字
            ('VAR',     r'VAR'),      # 变量声明关键字
            ('WHILE',   r'WHILE'),    # 循环关键字
            ('DO',      r'DO'),       # 执行关键字
            ('IF',      r'IF'),       # 条件判断关键字
            ('THEN',    r'THEN'),     # 条件成立时执行关键字
            ('NUMBER',  r'\d+'),                # 整数
            ('ID',      r'[A-Za-z][A-Za-z0-9]*'), # 标识符
            ('ASSIGN',  r':='),                 # 赋值运算符
            ('NE',      r'<>'),                 # 不等于运算符
            ('LE',      r'<='),                 # 小于等于运算符
            ('GE',      r'>='),                 # 大于等于运算符
            ('OP',      r'[+\-*/]'),            # 算术运算符
            ('LPAREN',  r'\('),                 # 左括号
            ('RPAREN',  r'\)'),                 # 右括号
            ('SEMICOLON', r';'),                # 分号
            ('COMMA',   r','),                  # 逗号
            ('NEWLINE', r'\n'),                 # 新行
            ('SKIP',    r'[ \t]+'),             # 跳过空格和制表符
            ('MISMATCH',r'.'),                  # 任何其他字符
        ]

    def tokenize(self):
        # 创建正则表达式并编译
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        get_token = re.compile(tok_regex).match
        pos = 0
        # 逐字符遍历源代码
        while pos < len(self.code):
            match = get_token(self.code, pos)
            if match is not None:
                type = match.lastgroup
                if type == 'NEWLINE':
                    # 更新行号和列号
                    self.current_line += 1
                    self.current_column = 1
                elif type != 'SKIP':
                    # 生成并添加 token
                    value = match.group(type)
                    token = Token(type, value, self.current_line, self.current_column)
                    self.tokens.append(token)
                pos = match.end()
                self.current_column += match.end() - match.start()
            else:
                # 处理无法匹配的字符
                raise RuntimeError(f'Unexpected character {self.code[pos]} at line {self.current_line} column {self.current_column}')
        return self.tokens

# 示例使用
if __name__ == "__main__":
    code = '''
    PROGRAM example;
    VAR x, y;
    BEGIN
        x := 2;
        IF x > 3 THEN
            y := x + 5;
        END;
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
