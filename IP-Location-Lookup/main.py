from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

import main_window

def main():
    window = main_window.Window()
    window.show()
    sys.exit(app.exec_())

app = QApplication(sys.argv)

if __name__ == '__main__':
    main()