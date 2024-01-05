from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QIcon, QPixmap, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import QHBoxLayout, QGraphicsView, QGraphicsScene, QDesktopWidget, \
    QGraphicsPixmapItem, QWidget, QPushButton, QScrollBar, QTextBrowser, QTextEdit, QLabel
from qframelesswindow import StandardTitleBar, FramelessDialog


class MyScrollBar(QScrollBar):
    def __init__(self, parent=None):
        super(MyScrollBar, self).__init__(parent)
        self.setStyleSheet("""
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
              QScrollBar:horizontal {
                  border-width: 0px;
                  border: none;
                  background:rgba(64, 65, 79, 0);
                  width:12px;
                  margin: 0px 0px 0px 0px;
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


class CodeEditorHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(CodeEditorHighlighter, self).__init__(parent)
        self.highlightingRules = []

        color = BasicColor()
        code_element_format = QTextCharFormat()
        code_element_format.setForeground(color.procedure_color)

    def set_highlighting_rules(self, dict):
        for key, value in dict.items():
            code_element_format = QTextCharFormat()
            code_element_format.setForeground(value)
            self.highlightingRules.append((QRegExp(key), code_element_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class ImagePushButton(QWidget):
    def __init__(self, path, height, parent=None):
        super().__init__(parent)
        pixmap = QPixmap(path)
        pixmap = pixmap.scaledToHeight(height)
        icon = QIcon(pixmap)
        button = QPushButton(self)
        self.clicked = button.clicked
        button.setIcon(icon)
        button.setIconSize(pixmap.size())
        color = BasicColor()
        button.setStyleSheet(f"""
            QPushButton{{background-color:{color.border_color.name()};border:None}}
            QPushButton:hover{{background-color:{color.bg_color.name()};}}
        """)

class BasicColor:
    def __init__(self):
        self.bg_color = QColor(40, 40, 40)
        self.border_color = QColor(60, 60, 60)
        self.hangover_color = QColor(50, 50, 50)
        self.menu_hangover_color = QColor(4, 57, 94)
        self.default_color = QColor(212, 212, 212)
        self.program_color = QColor(209, 105, 105)
        self.bracket_color = QColor(255, 215, 0)
        self.keyword_color = QColor(86, 156, 214)
        self.numbers_color = QColor(181, 206, 168)
        self.procedure_color = QColor(218, 112, 214)


class MyTitleBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)


class MyTitleBar(StandardTitleBar):

    def __init__(self, parent):
        super().__init__(parent)

        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(50, 50, 50))
        self.maxBtn.setHoverColor(Qt.white)
        self.maxBtn.setHoverBackgroundColor(QColor(50, 50, 50))
        self.closeBtn.setHoverColor(Qt.white)
        self.closeBtn.setHoverBackgroundColor(QColor(50, 50, 50))


class MyGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置场景的背景颜色
        self.setBackgroundBrush(QColor(60, 60, 60))


class ImageView(QGraphicsView):
    def __init__(self, path):
        super().__init__()

        scene = MyGraphicsScene(self)

        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(QSize(25, 25))
        pixmap_item = QGraphicsPixmapItem(pixmap)
        # 计算使 pixmap_item 居中的坐标值
        center_x = (scene.width() - pixmap.width()) / 2
        center_y = (scene.height() - pixmap.height()) / 2

        # 设置 pixmap_item 在场景中的位置
        pixmap_item.setPos(center_x, center_y)
        # scene.addWidget(pixmap_item, Qt.AlignCenter)
        scene.addItem(pixmap_item)


        self.setStyleSheet(f"""
                QGraphicsScene{{background-color:QColor(60, 60, 60);}}
                QGraphicsView{{border:solid rgba(0, 0, 0, 0);}}
            """)
        # scene.setSceneRect(pixmap_item.pixmap().rect())

        # 设置 QGraphicsView 的场景
        self.setScene(scene)


class ErrorPopup(FramelessDialog):
    def __init__(self, ex):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(QLabel(str(ex)), 0, Qt.AlignCenter)
        self.titleBar.raise_()
        self.resize(200, 100)
        self.setResizeEnabled(False)
        # self.setStyleSheet(f"""
        #     QWidget{{
        #                 background-color:{BasicColor().bg_color};
        #             }}
        # """)

    def center(self):
        # 获取屏幕的坐标系
        screen = QDesktopWidget().screenGeometry()

        # 获取窗口的坐标系
        size = self.geometry()

        # 计算窗口居中的坐标
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2

        # 移动窗口到居中的位置
        self.move(x, y)

class HelpPopup(FramelessDialog):
    def __init__(self):
        super().__init__()
