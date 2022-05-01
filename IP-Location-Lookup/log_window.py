from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import main_window

class LogWindow(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("IP Logs")
        self.setFixedSize(350, 200)
        self.setWindowIcon(QIcon('IP-Location-Lookup/img/icon.ico'))

        self.ips = main_window.Window.ip_list
        self.addItems(self.ips)

        self.clear_btn = QPushButton('Clear', self)
        self.clear_btn.setFont(QFont('Arial', 11))
        self.clear_btn.move(295, 170)
        self.clear_btn.resize(50, 25)
        self.clear_btn.clicked.connect(self.clear_click)

    def clear_click(self):
        self.clear()