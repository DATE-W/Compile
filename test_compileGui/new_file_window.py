# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\13293\Desktop\2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMenuBar, QMenu, QStatusBar, QTextEdit, QHBoxLayout
from qframelesswindow import FramelessMainWindow, FramelessDialog


class NewFileWindow(FramelessMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("新建文件")

        menuBar = QMenuBar(self.titleBar)