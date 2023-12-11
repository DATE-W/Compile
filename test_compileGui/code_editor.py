from PyQt5.QtWidgets import QPlainTextEdit, QScrollBar, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from tools import BasicColor
import sys


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        color = BasicColor()
        print(self.width())
        print(self.height())
        self.line_number_widget = QWidget(self)
        self.code_editor_widget = QWidget(self)
        print(self.line_number_widget.height())
        v_layout = QVBoxLayout(self.line_number_widget)
        v_layout.setContentsMargins(0, 0, 0, 0)
        h_layout = QHBoxLayout(self.code_editor_widget)
        h_layout.setContentsMargins(50, 0, 0, 0)

        self.line_numbers = QPlainTextEdit(self.line_number_widget)
        self.line_numbers.setReadOnly(True)
        self.line_numbers.setMaximumWidth(50)
        self.line_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.line_numbers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        self.code_editor = QPlainTextEdit(self.code_editor_widget)
        self.code_editor.setStyleSheet(f"""
                    QPlainTextEdit{{
                        border-left:1px solid rgba(60, 60, 60, 100);
                    }}
                """)
        v_layout.addWidget(self.line_numbers)
        h_layout.addWidget(self.code_editor, Qt.AlignCenter)
        self.code_editor.blockCountChanged.connect(self.update_line_number_area_width)
        self.code_editor.updateRequest.connect(self.update_scroll)
        self.code_editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setStyleSheet(f"""
                                QPlainTextEdit{{
                                    background-color:{color.bg_color.name()};
                                    color:{color.default_color.name()};
                                    border: none;
                                }}
                                """)
        self.line_numbers.setPlainText('1')
        # 修改code_editor的滚动条样式
        code_editor_scrollbar = QtWidgets.QScrollBar()
        code_editor_scrollbar.setStyleSheet("""
             QScrollBar:vertical {
                  border-width: 0px;
                  border: none;
                  background:rgba(64, 65, 79, 0);
                  width:12px;
                  margin: 0px 0px 0px 0px;
              }
              QScrollBar::handle:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0 #40414f, stop: 0.5 #40414f, stop:1 #40414f);
                  min-height: 20px;
                  max-height: 20px;
                  margin: 0 0px 0 0px;
                  border-radius: 6px;
              }
              QScrollBar::add-line:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
                  height: 0px;
                  border: none;
                  subcontrol-position: bottom;
                  subcontrol-origin: margin;
              }
              QScrollBar::sub-line:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
                  height: 0 px;
                  border: none;
                  subcontrol-position: top;
                  subcontrol-origin: margin;
              }
              QScrollBar::sub-page:vertical {
              background: rgba(64, 65, 79, 0);
              }

              QScrollBar::add-page:vertical {
              background: rgba(64, 65, 79, 0);
              }
              """)
        self.code_editor.setVerticalScrollBar(code_editor_scrollbar)

    # QScrollBar::handle: vertical
    # {{
    #      background: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 0,
    #  stop: 0  # aaaaff, stop: 0.5 #aaaaff, stop:1 #aaaaff);
    #  min - height: 20px;
    # max - height: 20
    # px;
    # margin: 0
    # 0
    # px
    # 0
    # 0
    # px;
    # border - radius: 6
    # px;
    # }}
    # QScrollBar::add - line: vertical
    # {{
    #      background: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 0,
    #  stop: 0 rgba(64, 65, 79, 0), stop: 0.5
    # rgba(64, 65, 79, 0), stop: 1
    # rgba(64, 65, 79, 0));
    # height: 0
    # px;
    # border: none;
    # subcontrol - position: bottom;
    # subcontrol - origin: margin;
    # }}
    # QScrollBar::sub - line: vertical
    # {{
    #      background: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 0,
    #  stop: 0  rgba(64, 65, 79, 0), stop: 0.5
    # rgba(64, 65, 79, 0), stop: 1
    # rgba(64, 65, 79, 0));
    # height: 0
    # px;
    # border: none;
    # subcontrol - position: top;
    # subcontrol - origin: margin;
    # }}
    # QScrollBar::sub - page: vertical
    # {{
    #     background: rgba(64, 65, 79, 0);
    # }}
    # QScrollBar::add - page: vertical
    # {{
    #     background: rgba(64, 65, 79, 0);
    # }}

    def update_line_number_area_width(self):

        digits = len(str(self.code_editor.blockCount()))
        width = 10 + self.code_editor.fontMetrics().width('1') * digits
        self.line_number_widget.setMinimumWidth(width)
        block_count = self.code_editor.blockCount()

        line_text = ''
        for i in range(block_count):
            line_text += str(i + 1) + '\n'
        self.line_numbers.setPlainText(line_text)
        self.line_numbers.ensureCursorVisible()
        # if block_count > 40:
        #     block = self.line_numbers.document().findBlockByLineNumber(3)
        #     cursor = QTextCursor(block)
        #     cursor.insertText('a')

    def update_scroll(self, rect, dy):
        if dy:
            self.line_numbers.scroll(0, dy)
            return
        # visible_blocks = self.visibleBlocks()


# class CodeEditor(QPlainTextEdit):
#     def __init__(self, parent = None):
#         super(CodeEditor, self).__init__(parent)
#         color = BasicColor()
#         # PL/0 词法规则定义
#         self.token_specification = {
#             'PROGRAM': (r'PROGRAM', color.program_color),  # 程序开始关键字
#             'BEGIN': (r'BEGIN', color.procedure_color),  # 开始关键字
#             'END': r'END',  # 结束关键字
#             'CONST': r'CONST',  # 常量声明关键字
#             'VAR': r'VAR',  # 变量声明关键字
#             'WHILE': r'WHILE',  # 循环关键字
#             'DO': r'DO',  # 执行关键字
#             'IF': r'IF',  # 条件判断关键字
#             'THEN': r'THEN',  # 条件成立时执行关键字
#             'NUMBER': r'\d+',  # 整数
#             'ID': r'[A-Za-z][A-Za-z0-9]*',  # 标识符
#             'ASSIGN': r':=',  # 赋值运算符
#             'NE': r'<>',  # 不等于运算符
#             'LE': r'<=',  # 小于等于运算符
#             'GE': r'>=',  # 大于等于运算符
#             'EQ': r'=',  # 判等运算符
#             'GR': r'>',  # 小于运算符
#             'LS': r'<',  # 大于运算符
#             # 'OP': r'[+-*/]',
#             'ADD': r'\+',  # 加法运算符
#             'SUB': r'\-',  # 减法运算符
#             'MUL': r'\*',  # 乘法运算符
#             'DIV': r'/',  # 除法运算符
#             'LPAREN': r'\(',  # 左括号
#             'RPAREN': r'\)',  # 右括号
#             'SEMICOLON': r';',  # 分号
#             'COMMA': r',',  # 逗号
#             'NEWLINE': r'\n',  # 新行
#             'SKIP': r'[ \t]+',  # 跳过空格和制表符
#             'MISMATCH': r'.',  # 任何其他字符
#         }
#         self.line_number_widget = QWidget(self)
#         v_layout = QVBoxLayout(self.line_number_widget)
#         v_layout.setContentsMargins(0, 0, 0, 0)
#
#         self.line_numbers = QPlainTextEdit(self.line_number_widget)
#         self.line_numbers.setReadOnly(True)
#         self.line_numbers.setMaximumWidth(50)
#         self.line_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.line_numbers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.line_numbers.setStyleSheet(f"""
#             QPlainTextEdit{{
#                 border-right:1px solid rgba(60, 60, 60, 100);
#             }}
#         """)
#         v_layout.addWidget(self.line_numbers)
#         self.blockCountChanged.connect(self.update_line_number_area_width)
#         self.updateRequest.connect(self.update_scroll)
#
#
#         self.setStyleSheet(f"""
#                                     QPlainTextEdit{{
#                                         background-color:{color.bg_color.name()};
#                                         color:{color.default_color.name()};
#                                         border: none;
#                                     }}
#                                     QScrollBar{{background-color:
#                                         color:{color.default_color.name()}{color.bg_color.name()};}}
#                                 """)
#         self.line_numbers.setPlainText('1')
#
#     # 更新行号区域宽度与行号
#     def update_line_number_area_width(self):
#         digits = len(str(self.blockCount()))
#         width = 10 + self.fontMetrics().width('1') * digits
#         self.line_number_widget.setMinimumWidth(width)
#
#
#         block_count = self.blockCount()
#
#         line_text = ''
#         for i in range(block_count):
#             line_text += str(i + 1) + '\n'
#
#
#
#         self.line_numbers.setPlainText(line_text)
#         self.line_numbers.ensureCursorVisible()
#         block = self.line_numbers.document().findBlockByLineNumber(0)
#         cursor = QTextCursor(block)
#         # cursor.insertText('test!')
#         # cursor.insertText(line_text)
#         print(cursor.blockNumber())
#
#     # 更新行号
#     def update_scroll(self, rect, dy):
#         if dy:
#             self.line_numbers.scroll(0, dy)
#             return
#         # visible_blocks = self.visibleBlocks()
#
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        print('resized!!')
        digits = len(str(max(1, self.blockCount())))
        print(cr.height())
        self.code_editor_widget.setGeometry(10 + self.fontMetrics().width('1') * digits, cr.top(),
                                            cr.right()-cr.left() - 18, cr.height())
        self.line_number_widget.setGeometry(cr.left(), cr.top(), 10 + self.fontMetrics().width('1') * digits, 50000)
        print(self.line_number_widget.height())
