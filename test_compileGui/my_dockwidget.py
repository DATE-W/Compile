import sys

from PyQt5.QtWidgets import QDockWidget
from tools import CustomTitleBar
from qframelesswindow import FramelessMainWindow, FramelessDialog, StandardTitleBar


class MyDockWidget(QDockWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setTitleBar(CustomTitleBar(self))
        # self.menuBar =
