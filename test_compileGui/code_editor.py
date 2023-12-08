from PyQt5.QtWidgets import QPlainTextEdit, QScrollBar
from PyQt5.QtGui import QFont, QColor
import sys


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent = None):
        super(CodeEditor, self).__init__(parent)
        self.bg_color = QColor(40, 40, 40)
        self.program_color = QColor(209, 105, 105)
        self.bracket_color = QColor(255, 215, 0)
        self.keyword_color = QColor(86, 156, 214)
        self.numbers_color = QColor(181, 206, 168)
        self.default_color = QColor(212, 212, 212)
        self.procedure_color = QColor(218, 112, 214)
        # PL/0 词法规则定义
        self.token_specification = {
            'PROGRAM': (r'PROGRAM', self.program_color),  # 程序开始关键字
            'BEGIN': (r'BEGIN', self.procedure_color),  # 开始关键字
            'END': r'END',  # 结束关键字
            'CONST': r'CONST',  # 常量声明关键字
            'VAR': r'VAR',  # 变量声明关键字
            'WHILE': r'WHILE',  # 循环关键字
            'DO': r'DO',  # 执行关键字
            'IF': r'IF',  # 条件判断关键字
            'THEN': r'THEN',  # 条件成立时执行关键字
            'NUMBER': r'\d+',  # 整数
            'ID': r'[A-Za-z][A-Za-z0-9]*',  # 标识符
            'ASSIGN': r':=',  # 赋值运算符
            'NE': r'<>',  # 不等于运算符
            'LE': r'<=',  # 小于等于运算符
            'GE': r'>=',  # 大于等于运算符
            'EQ': r'=',  # 判等运算符
            'GR': r'>',  # 小于运算符
            'LS': r'<',  # 大于运算符
            # 'OP': r'[+-*/]',
            'ADD': r'\+',  # 加法运算符
            'SUB': r'\-',  # 减法运算符
            'MUL': r'\*',  # 乘法运算符
            'DIV': r'/',  # 除法运算符
            'LPAREN': r'\(',  # 左括号
            'RPAREN': r'\)',  # 右括号
            'SEMICOLON': r';',  # 分号
            'COMMA': r',',  # 逗号
            'NEWLINE': r'\n',  # 新行
            'SKIP': r'[ \t]+',  # 跳过空格和制表符
            'MISMATCH': r'.',  # 任何其他字符
        }
        self.init_ui()



    def init_ui(self):
        # self.setStyleSheet(f"QPlainTextEdit {{ background-color: {self.bg_color.name()};border: none; "
        #                    f"color: {self.default_color.name()}}}")
        self.setStyleSheet(f"""
                            QPlainTextEdit{{
                                background-color:{self.bg_color.name()}; 
                                border: none;
                                color:{self.default_color.name()};
                            }}
                            QScrollBar{{background-color:{self.bg_color.name()};}}
                        """)
    #     # 创建一个新字体
    #     font = QFont()
    #     font.setFamily("Courier")  # 设置字体
    #     font.setPointSize(12)  # 设置字体大小
    #     font.setBold(True)  # 设置为粗体
    #
    #     # 应用新字体到文本编辑器
    #     self.setFont(font)