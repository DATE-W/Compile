import sys
from src.gui.windows import Ui_MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = Ui_MainWindow()
    main_window.show()

    sys.exit(app.exec_())
