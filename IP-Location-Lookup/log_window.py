from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import main_window

class LogWindow(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Logs")
        self.setWindowIcon(QIcon('icon.ico'))
        self.ips = main_window.Window.ip_dict

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.list_widget = QListWidget(self)
        self.list_widget.addItems(self.ips.keys())
        self.list_widget.setFont(QFont('Arial', 11))
        self.layout.addWidget(self.list_widget)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.clear_btn = QPushButton('Clear')
        self.clear_btn.setFont(QFont('Arial', 11))
        self.clear_btn.clicked.connect(self.clear_btn_click)
        self.button_layout.addWidget(self.clear_btn)

        self.export_btn = QPushButton('Export')
        self.export_btn.setFont(QFont('Arial', 11))
        self.export_btn.clicked.connect(self.export_btn_click)
        self.button_layout.addWidget(self.export_btn)

        self.setLayout(self.layout)

    def clear_btn_click(self):
        self.findChild(QListWidget).clear()
        self.ips.clear()
    
    def export_btn_click(self):
        if self.ips == {}:
            QMessageBox.information(self, "Export", "No IPs to export.")
            return
        if not os.path.exists('exports'):
            os.makedirs('exports')

        os.chdir('exports')
        with open('ips.txt', 'w') as self.file:
            self.file.write('[IPs]\n\n')
            for self.ip, self.info in self.ips.items():
                self.file.write(self.ip + '\n')
                self.file.write(' ' + self.info + '\n\n')
        os.chdir(main_window.Window.owd)