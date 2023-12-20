from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QHBoxLayout, QVBoxLayout

from .tools import BasicColor, CodeEditorHighlighter


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        color = BasicColor()
        # print(self.width())
        # print(self.height())
        self.line_number_widget = QWidget(self)
        self.code_editor_widget = QWidget(self)
        # print(self.line_number_widget.height())
        v_layout = QVBoxLayout(self.line_number_widget)
        v_layout.setContentsMargins(0, 0, 0, 0)
        h_layout = QHBoxLayout(self.code_editor_widget)
        h_layout.setContentsMargins(30, 0, 0, 0)

        self.line_numbers = QPlainTextEdit(self.line_number_widget)
        self.line_numbers.setReadOnly(True)
        self.line_numbers.setMaximumWidth(30)
        self.line_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.line_numbers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # cr = self.contentsRect()
        # self.line_number_widget.setGeometry(cr.left(), cr.top(), 10 + self.fontMetrics().width('1') * 1, 50000)

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
        # self.code_editor.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.currentLineNumber = -1
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
              QScrollBar::handle:horizontal {
                  background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                  stop: 0 #40414f, stop: 0.5 #40414f, stop:1 #40414f);
                  min-height: 20px;
                  max-height: 20px;
                  margin: 0 0px 0 0px;
                  border-radius: 6px;
              }
              QScrollBar::add-line:horizontal {
                  background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                  stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
                  height: 0px;
                  border: none;
                  subcontrol-position: bottom;
                  subcontrol-origin: margin;
              }
              QScrollBar::sub-line:horizontal {
                  background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                  stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
                  height: 0 px;
                  border: none;
                  subcontrol-position: top;
                  subcontrol-origin: margin;
              }
              QScrollBar::sub-page:horizontal {
              background: rgba(64, 65, 79, 0);
              }

              QScrollBar::add-page:horizontal {
              background: rgba(64, 65, 79, 0);
              }
              """)
        self.code_editor.setVerticalScrollBar(code_editor_scrollbar)
        self.setHighlighter()

    def update_line_number_area_width(self):
        # print('changed')
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        # print('resized!!')
        digits = len(str(max(1, self.blockCount())))
        # print(cr.height())
        self.code_editor_widget.setGeometry(10 + self.fontMetrics().width('1') * digits, cr.top(),
                                            cr.right()-cr.left() - 18, cr.height())
        self.line_number_widget.setGeometry(cr.left(), cr.top(), 10 + self.fontMetrics().width('1') * digits, 50000)
        # print(self.line_number_widget.height())

    def setHighlighter(self):
        color = BasicColor()
        highlight_dict = {
            r'\bPROGRAM\b': color.program_color,  # 程序开始关键字
            r'\bBEGIN\b': color.procedure_color,  # 开始关键字
            r'\bEND\b': color.procedure_color,  # 结束关键字
            r'\bCONST\b': color.keyword_color,  # 常量声明关键字
            r'\bVAR\b': color.keyword_color,  # 变量声明关键字
            r'\bWHILE\b': color.keyword_color,  # 循环关键字
            r'\bDO\b': color.keyword_color,  # 执行关键字
            r'\bIF\b': color.keyword_color,  # 条件判断关键字
            r'\bTHEN\b': color.keyword_color,  # 条件成立时执行关键字
            # 'num': r'\d+',  # 整数
            # 'id': r'[a-z][a-z0-9]*',  # 标识符
            # 'ASSIGN': r':=',  # 赋值运算符
            # 'NE': r'<>',  # 不等于运算符
            # 'LE': r'<=',  # 小于等于运算符
            # 'GE': r'>=',  # 大于等于运算符
            # 'EQ': r'=',  # 判等运算符
            # 'GR': r'>',  # 小于运算符
            # 'LS': r'<',  # 大于运算符
            # # 'OP': r'[+-*/]',
            # 'ADD': r'\+',  # 加法运算符
            # 'SUB': r'\-',  # 减法运算符
            # 'MUL': r'\*',  # 乘法运算符
            # 'DIV': r'/',  # 除法运算符
            r'\(': color.bracket_color,  # 左括号
            r'\)': color.bracket_color,  # 右括号
        }
        self.highlighter = CodeEditorHighlighter(self.code_editor.document())
        self.highlighter.set_highlighting_rules(highlight_dict)

    # def highlightCurrentLine(self):
    #     newCurrentLineNumber = self.textCursor().blockNumber()
    #     if newCurrentLineNumber != self.currentLineNumber:
    #         self.currentLineNumber = newCurrentLineNumber
    #         hi_selection = QTextEdit.ExtraSelection()
    #         hi_selection.format.setBackground((self.currentLineColor))
    #         hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
    #         hi_selection.cursor = self.textCursor()
    #         hi_selection.cursor.clearSelection()
    #         self.setExtraSelections([hi_selection])