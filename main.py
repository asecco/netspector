from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Location Lookup")
        self.setFixedSize(600, 300)
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
        self.textbox.move(100, 30)
        self.textbox.resize(400, 35)

        self.button = QPushButton("Lookup", self)
        self.button.move(240, 75)
        self.button.resize(125, 40)
        self.button.clicked.connect(self.button_click)

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.move(100, 135)
        self.label.resize(400, 150)

        self.shortcut = QShortcut(QKeySequence("RETURN"), self)
        self.shortcut.activated.connect(self.enter_shortcut)

    def button_click(self):
        textbox_value = self.textbox.text()
        request = requests.get("http://ip-api.com/json/" + textbox_value).json()
        self.label.setText(str(request))

    def enter_shortcut(self):
        self.button.click()

    def about_button(self):
        QMessageBox.about(self, "About", "Created By: Andrew Secco\n\nhttps://github.com/asecco")

    def exit_button(self):
        sys.exit()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())