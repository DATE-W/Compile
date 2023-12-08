

class CustomTitleBar(StandardTitleBar):

    def __init__(self, parent):
        super().__init__(parent)

        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(50, 50, 50))
        self.maxBtn.setHoverColor(Qt.white)
        self.maxBtn.setHoverBackgroundColor(QColor(50, 50, 50))
        self.closeBtn.setHoverColor(Qt.white)
        self.closeBtn.setHoverBackgroundColor(QColor(50, 50, 50))
