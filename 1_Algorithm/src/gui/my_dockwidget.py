from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QRadioButton, QHBoxLayout, QTextEdit, QTableWidget, QWidget

from .tools import MyTitleBarWidget, BasicColor


class MyDockWidget(QDockWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        my_title_bar = MyTitleBarWidget()
        self.table = QTableWidget()
        self.mcode = QTextEdit()
        self.mcode.setReadOnly(True)
        self.setTitleBarWidget(my_title_bar)
        self.setWidget(self.table)
        # check_box = QCheckBox('check me', self)
        # my_title_bar.h_layout.addWidget(check_box, Qt.AlignCenter)
        self.setFixedHeight(200)

        # output_button = QRadioButton('输出', self)
        table_button = QRadioButton('LR1分析表', self)
        mcode_button = QRadioButton('中间代码', self)
        table_button.setChecked(True)
        table_button.toggled.connect(self.show_table)
        mcode_button.toggled.connect(self.show_mcode)
        # minimize_button = ImagePushButton('pic/icon_minimize.png', 15, self)
        # minimize_button.setMinimumHeight(25)

        #
        # my_title_bar.h_layout.addWidget(output_button, Qt.AlignCenter)
        my_title_bar.h_layout.addWidget(table_button, Qt.AlignCenter)
        my_title_bar.h_layout.addWidget(mcode_button, Qt.AlignCenter)
        # my_title_bar.h_layout.addWidget(minimize_button, Qt.AlignAbsolute)
        # minimize_button.clicked.connect(super().showMinimized)

        color = BasicColor()
        self.setStyleSheet(f"""
            QRadioButton{{color:{color.default_color.name()};}}
        """)
        #
        #
        # button_group = QButtonGroup(self)
        # button_group.addButton(self.output_button)
        # button_group.addButton(self.table_button)
        # button_group.addButton(self.mcode_button)
    def show_table(self):
        self.setWidget(self.table)

    def show_mcode(self):
        self.setWidget(self.mcode)

