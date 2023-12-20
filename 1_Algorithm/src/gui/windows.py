# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\13293\Desktop\1.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QMenuBar, QMenu, QHBoxLayout, QTableWidgetItem
from qframelesswindow import FramelessMainWindow, FramelessDialog

from .code_editor import CodeEditor
from .my_dockwidget import MyDockWidget
from .code_runner import code_runner
from .tools import MyTitleBar, ImageView


class Ui_MainWindow(FramelessMainWindow):

    def __init__(self):
        self.bg_color = QColor(40, 40, 40)
        self.border_color = QColor(60, 60, 60)
        self.hangover_color = QColor(50, 50, 50)
        self.menu_hangover_color = QColor(4, 57, 94)
        self.default_color = QColor(212, 212, 212)
        super().__init__()
        self.setWindowTitle("新建文件")

        # add menu bar
        self.setTitleBar(MyTitleBar(self))
        # self.setWindowIcon(QIcon('pic/vscode.png'))
        self.menuBar = QMenuBar(self.titleBar)
        self.pictureBox = ImageView('pic/edocsv.png')
        self.pictureBox.setFixedWidth(35)
        menu = QMenu('文件', self)
        menu.addAction('新建')
        menu.addAction('打开')
        self.menuBar.addMenu(menu)
        self.menuBar.addAction('运行', self.run)
        self.menuBar.addAction('帮助', self.showHelpDialog)
        self.titleBar.layout().insertWidget(1, self.menuBar, 0, Qt.AlignLeft)
        self.titleBar.layout().insertWidget(0, self.pictureBox, 0, Qt.AlignCenter)
        self.titleBar.layout().setSpacing(0)
        self.titleBar.layout().insertStretch(1, 0)
        self.setMenuWidget(self.titleBar)

        self.codeEditor = CodeEditor(self)
        self.setCentralWidget(self.codeEditor)

        # set QDockWidget
        self.dock = MyDockWidget('dock', self)
        self.dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock)

        self.setStyleSheet(f"""
                FramelessMainWindow{{background-color:{self.border_color.name()};}}
                QMenuBar{{background-color:{self.border_color.name()};padding: 3px 0px 0px 0px; color:{self.default_color.name()};border:none;}}
                QMenuBar::item:selected{{background-color:{self.hangover_color.name()}}}
                QMenu{{background-color:{self.border_color.name()};color:{self.default_color.name()}}}
                QMenu:selected{{background-color:{self.menu_hangover_color.name()}}}
                QTextEdit{{background-color:{self.bg_color.name()};border: none; font-size: 15px}}
                QStatusBar{{background-color:{self.bg_color.name()};bordr: none}}
                QMainWindow::close-button{{background-color:{self.default_color.name()};}}
                QTableWidget{{background-color:{self.bg_color.name()};color:{self.default_color.name()};border:None}}
                QHeaderView{{background:{self.bg_color.name()};}}
                """)
        self.codeEditor.setGeometry(100, 100, 500, 400)
        self.setGeometry(100, 100, 600, 600)


    def showHelpDialog(self):
        w = FramelessDialog(self)

        # add a label to dialog
        w.setLayout(QHBoxLayout())
        w.layout().addWidget(QLabel('Frameless Dialog'), 0, Qt.AlignCenter)

        # raise title bar
        w.titleBar.raise_()
        w.resize(300, 300)

        # disable resizing dialog
        w.setResizeEnabled(False)
        w.exec()

    def run(self):
        content = self.codeEditor.code_editor.toPlainText()
        table, output = code_runner(content)

        # 找到主窗口中的 MyDockWidget 实例
        # dock_widget = self.findChild(MyDockWidget, 'dock')  # 'dock' 是您在创建时设置的对象名称
        # print(table)
        print(output)
        # 如果找到了 MyDockWidget 实例
        if self.dock:
            # 调用一个函数来填充 MyDockWidget 中的 QTableWidget
            self.fill_table_with_dict_list(self.dock.table, table)
            self.fill_mcode_with_codegen(self.dock.mcode, output)

    def fill_table_with_dict_list(self, table_widget, dict_list):
        # 确保有数据
        if not dict_list:
            return

        # 获取所有键作为表头
        headers = list(dict_list[0].keys())
        # print(headers)
        table_widget.setColumnCount(len(headers))
        table_widget.setRowCount(len(dict_list))
        table_widget.setHorizontalHeaderLabels(headers)

        # 填充数据
        for row_index, row_dict in enumerate(dict_list):
            for col_index, header in enumerate(headers):
                # 这里不知道为什么row_dict都是0，1，2这种索引
                item_value = dict_list[row_index].get(header, '')
                table_widget.setItem(row_index, col_index, QTableWidgetItem(item_value))

        # 调整列宽以适应内容
        table_widget.resizeColumnsToContents()

    def fill_mcode_with_codegen(self, mcode_widget, codegen):
        mcode_widget.setText(codegen)


