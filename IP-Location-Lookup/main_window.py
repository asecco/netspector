from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarktheme
import sys
import requests
import pprint
import re
import os
import configparser
import main
import log_window

class Window(QMainWindow):
    ip_dict = {}
    owd = os.getcwd()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Location Lookup")
        self.setFixedSize(680, 500)
        self.setWindowIcon(QIcon('icon.ico'))
        main.app.setStyleSheet(qdarktheme.load_stylesheet("light"))
        self.config = configparser.ConfigParser()

        self.init_ui()
        self.show()

    def init_ui(self):
        self.create_menu()

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("69.89.31.226")
        self.textbox.move(60, 35)
        self.textbox.resize(400, 35)

        self.lookup_btn = QPushButton("Lookup", self)
        self.lookup_btn.setFont(QFont('Arial', 11))
        self.lookup_btn.move(470, 35)
        self.lookup_btn.resize(115, 35)
        self.lookup_btn.clicked.connect(self.lookup_btn_click)

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setFont(QFont('Arial', 10))
        self.label.move(420, 190)
        self.label.resize(400, 180)

        self.map_label = QLabel(self)
        self.map_label.move(15, 85)
        self.map_label.resize(400, 400)

        self.dt_checkbox = QCheckBox('Dark Theme', self)
        self.dt_checkbox.move(560, 470)
        self.dt_checkbox.stateChanged.connect(self.checkbox_click)

        self.shortcut = QShortcut(QKeySequence("RETURN"), self)
        self.shortcut.activated.connect(self.lookup_btn_click)

        self.create_config()
        self.read_config()
    
    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about_btn_click)
        file_menu.addAction(about_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_btn_click)
        file_menu.addAction(exit_action)

        tools_menu = menubar.addMenu("Tools")
        logs_action = QAction("IP Logs", self)
        logs_action.triggered.connect(self.logs_btn_click)
        tools_menu.addAction(logs_action)
    
    def lookup_btn_click(self):
        self.textbox_value = self.textbox.text().strip()
        self.request = requests.get(f"http://ip-api.com/json/{self.textbox_value}?fields=country,regionName,city,zip,isp,proxy,message,lat,lon").json()
        self.request = pprint.pformat(self.request, sort_dicts=False).replace('{', '').replace('}', '').replace("'", '')
        self.label.setText(' ' + str(self.request))
        self.map_label.setStyleSheet("border: 2px solid black;")

        if self.textbox_value != '' and self.request != 'message: invalid query':
            self.ip_dict[self.textbox_value] = str(self.request)
        
        if self.request != 'message: invalid query' and self.request != 'message: private range':
            self.map_coordinates(self.request)
            self.map_label.setHidden(False)
            self.label.move(420, 190)
            self.textbox.setStyleSheet("")
        else:
            self.map_label.setHidden(True)
            self.label.move(240, 160)
            self.textbox.setStyleSheet("border: 1px solid red;")
    
    def map_coordinates(self, r):
        self.lat = re.search(r'lat:\s(.*)', r).group().replace('lat: ', '')
        self.lon = re.search(r'lon:\s(.*)', r).group().replace('lon: ', '')

        self.map_url = f"https://cache.ip-api.com/{self.lon}{self.lat}10"
        self.map = QImage()
        self.map.loadFromData(requests.get(self.map_url).content)
        self.map_label.setPixmap(QPixmap(self.map))

    def create_config(self):
        if not os.path.exists('settings'):
            os.makedirs('settings')
            os.chdir('settings')
            self.config['GENERAL'] = {'darkmode': 'False'}
            with open('settings.ini', 'w') as self.settings_file:
                self.config.write(self.settings_file)            
            os.chdir(self.owd)

    def read_config(self):
        os.chdir('settings')
        self.config.read('settings.ini')
        if self.config['GENERAL']['darkmode'] == 'True':
            main.app.setStyleSheet(qdarktheme.load_stylesheet())
            self.dt_checkbox.setChecked(True)
        else:
            main.app.setStyleSheet(qdarktheme.load_stylesheet("light"))
            self.dt_checkbox.setChecked(False)
        os.chdir(self.owd)

    def checkbox_click(self):
        os.chdir(self.owd)
        os.chdir('settings')
        self.config.read('settings.ini')
        if self.dt_checkbox.isChecked():
            main.app.setStyleSheet(qdarktheme.load_stylesheet())
            self.config.set('GENERAL', 'darkmode', 'True')
        else:
            main.app.setStyleSheet(qdarktheme.load_stylesheet("light"))
            self.config.set('GENERAL', 'darkmode', 'False')
        
        with open('settings.ini', 'w') as self.settings_file:
            self.config.write(self.settings_file)
        os.chdir(self.owd)

    def logs_btn_click(self):
        self.log_window = log_window.LogWindow()
        self.log_window.show()

    def about_btn_click(self):
        QMessageBox.about(self, "About", "Created By: Andrew Secco\n\nhttps://github.com/asecco")

    def exit_btn_click(self):
        sys.exit()