from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import socket
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Location Lookup")
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

        self.textbox = QLineEdit(self)
        self.textbox.move(90, 30)
        self.textbox.resize(400, 35)

        self.button = QPushButton("Lookup", self)
        self.button.move(230, 75)
        self.button.resize(125, 40)
        self.button.clicked.connect(self.button_click)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(s.getsockname()[0])
        s.close()

    def button_click(self):
        request = requests.get("http://ip-api.com/json/24.48.0.1").json()
        print(request)


    def about_button(self):
        QMessageBox.about(self, "About", "Created By: Andrew Secco\n\nhttps://github.com/asecco")

    def exit_button(self):
        sys.exit()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())