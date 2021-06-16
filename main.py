from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anonymous Profile Viewer")
        self.setGeometry(670, 350, 600, 300)
        self.setWindowIcon(QIcon('icon.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)

        self.init_ui()
        self.show()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("About", self.about_button)
        file_menu.addAction("Exit", self.exit_button)

        self.button = QPushButton("Run", self)
        self.button.move(230, 40)
        self.button.resize(125, 40)
        self.button.clicked.connect(self.button_click)


    def button_click(self):
        self.show()

    def exit_button(self):
        sys.exit()

    def about_button(self):
        QMessageBox.about(self, "About", "Created By: Andrew Secco\n\nhttps://github.com/asecco")


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())