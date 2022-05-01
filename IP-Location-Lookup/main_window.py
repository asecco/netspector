from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarktheme
import sys
import requests
import pprint
import re

import main
import log_window

class Window(QMainWindow):
    ip_list = []
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Location Lookup")
        self.setFixedSize(650, 500)
        self.setWindowIcon(QIcon('IP-Location-Lookup/img/icon.ico'))
        main.app.setStyleSheet(qdarktheme.load_stylesheet("light"))

        self.init_ui()
        self.show()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("About", self.about_btn_click)
        file_menu.addAction("Exit", self.exit_btn_click)

        file_menu = menubar.addMenu("Tools")
        file_menu.addAction("IP Logs", self.logs_btn_click)

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("69.89.31.226")
        self.textbox.move(60, 30)
        self.textbox.resize(400, 35)

        self.lookup_btn = QPushButton("Lookup", self)
        self.lookup_btn.setFont(QFont('Arial', 11))
        self.lookup_btn.move(470, 30)
        self.lookup_btn.resize(115, 35)
        self.lookup_btn.clicked.connect(self.lookup_btn_click)

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setFont(QFont('Arial', 12))
        self.label.move(420, 190)
        self.label.resize(400, 180)

        self.map_label = QLabel(self)
        self.map_label.move(15, 85)
        self.map_label.resize(400, 400)

        self.dt_checkbox = QCheckBox('Dark Theme', self)
        self.dt_checkbox.move(560, 470)
        self.dt_checkbox.stateChanged.connect(self.checkbox_click)

        self.shortcut = QShortcut(QKeySequence("RETURN"), self)
        self.shortcut.activated.connect(self.enter_shortcut)
    
    def lookup_btn_click(self):
        self.textbox_value = self.textbox.text().strip()
        if self.textbox_value != '':
            self.ip_list.append(self.textbox_value)

        self.request = requests.get("http://ip-api.com/json/" + self.textbox_value + "?fields=country,regionName,city,zip,isp,proxy,message,lat,lon").json()
        self.request = pprint.pformat(self.request, sort_dicts=False).replace('{', '').replace('}', '').replace("'", '')
        self.label.setText(str(self.request))
        self.map_label.setStyleSheet("border: 1px solid black;")
        self.map_coordinates(self.request)
    
    def map_coordinates(self, r):
        self.lat = re.search(r'lat:\s(.*)', r)
        self.lat = self.lat.group().replace('lat: ', '')

        self.lon = re.search(r'lon:\s(.*)', r)
        self.lon = self.lon.group().replace('lon: ', '')

        self.map_url = "https://cache.ip-api.com/" + self.lon + self.lat + '10'
        self.map = QImage()
        self.map.loadFromData(requests.get(self.map_url).content)
        self.map_label.setPixmap(QPixmap(self.map))

    def checkbox_click(self):
        if self.dt_checkbox.isChecked():
          main.app.setStyleSheet(qdarktheme.load_stylesheet())
        else:
          main.app.setStyleSheet(qdarktheme.load_stylesheet("light"))

    def enter_shortcut(self):
        self.lookup_btn.click()

    def logs_btn_click(self):
        self.log_window = log_window.LogWindow()
        self.log_window.show()

    def about_btn_click(self):
        QMessageBox.about(self, "About", "Created By: Andrew Secco\n\nhttps://github.com/asecco")

    def exit_btn_click(self):
        sys.exit()