from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

import main_window

class LogWindow(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("IP Logs")
        self.setFixedSize(350, 200)
        self.setWindowIcon(QIcon('IP-Location-Lookup/img/icon.ico'))
        self.setFont(QFont('Arial', 12))

        self.ips = main_window.Window.ip_list
        self.addItems(self.ips)

        self.clear_btn = QPushButton('Clear', self)
        self.clear_btn.setFont(QFont('Arial', 11))
        self.clear_btn.move(295, 170)
        self.clear_btn.resize(50, 25)
        self.clear_btn.clicked.connect(self.clear_btn_click)

        self.export_btn = QPushButton('Export', self)
        self.export_btn.setFont(QFont('Arial', 11))
        self.export_btn.move(245, 170)
        self.export_btn.resize(50, 25)
        self.export_btn.clicked.connect(self.export_btn_click)

    def clear_btn_click(self):
        self.clear()
        self.ips.clear()
    
    def export_btn_click(self):
        if not os.path.exists('IP-Location-Lookup/exports'):
            os.makedirs('IP-Location-Lookup/exports')

        os.chdir('IP-Location-Lookup/exports')
        with open('ips.txt', 'w') as self.file:
            self.header = '[IPs]'
            self.file.write(self.header + '\n')
            for self.ip in self.ips:
                self.file.write(self.ip + '\n')
        os.chdir(main_window.Window.owd)