from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QIcon, QPixmap, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import QHBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QWidget, QPushButton
from qframelesswindow import StandardTitleBar


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
