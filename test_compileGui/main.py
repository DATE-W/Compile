# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from windows import Ui_MainWindow


# class MyMainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super(MyMainWindow, self).__init__()
#         # self.setup_ui(self)
#     # Use a breakpoint in the code line below to debug your script.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = Ui_MainWindow()
    main_window.show()

    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
