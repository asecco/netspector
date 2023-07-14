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
from scapy.layers.inet import IP, sr1, UDP
import main
import log_window

class Window(QMainWindow):
    ip_dict = {}
    owd = os.getcwd()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Location Lookup")
        self.setWindowIcon(QIcon('icon.ico'))
        main.app.setStyleSheet(qdarktheme.load_stylesheet("light"))
        self.config = configparser.ConfigParser()

        self.init_ui()
        self.show()

    def init_ui(self):
        self.create_menu()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.form_layout = QFormLayout()
        self.textbox = QLineEdit()
        self.textbox.setPlaceholderText("69.89.31.226")
        self.form_layout.addRow("IP Address:", self.textbox)

        self.lookup_btn = QPushButton("Lookup")
        self.lookup_btn.setFont(QFont('Arial', 11))
        self.lookup_btn.clicked.connect(self.lookup_btn_click)

        self.traceroute_btn = QPushButton("Traceroute")
        self.traceroute_btn.setFont(QFont('Arial', 11))
        self.traceroute_btn.clicked.connect(self.traceroute_btn_click)

        self.form_layout.addRow("", self.lookup_btn)
        self.form_layout.addRow("", self.traceroute_btn)

        self.layout.addLayout(self.form_layout)

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setFont(QFont('Arial', 11))
        self.label.setMinimumHeight(200)
        self.label.setAlignment(Qt.AlignTop)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)
        self.layout.addWidget(scroll_area)

        self.map_label = QLabel()
        self.map_label.setHidden(True)
        self.layout.addWidget(self.map_label, stretch=1)
        self.layout.setAlignment(self.map_label, Qt.AlignCenter)

        self.dt_checkbox = QCheckBox('Dark Theme')
        self.dt_checkbox.stateChanged.connect(self.checkbox_click)
        self.layout.addWidget(self.dt_checkbox)

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
        self.label.setText('' + str(self.request))
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
            self.textbox.setStyleSheet("border: 2px solid red;")
    
    def map_coordinates(self, r):
        self.lat = re.search(r'lat:\s(.*)', r).group().replace('lat: ', '')
        self.lon = re.search(r'lon:\s(.*)', r).group().replace('lon: ', '')

        self.map_url = f"https://cache.ip-api.com/{self.lon}{self.lat}10"
        self.map = QImage()
        self.map.loadFromData(requests.get(self.map_url).content)
        self.map_label.setPixmap(QPixmap(self.map))
    
    def traceroute_btn_click(self):
        self.hostname = self.textbox.text().strip()
        self.traceroute = ''
        self.map_label.setHidden(True)
        self.label.setText('' + self.traceroute)
        for i in range(1, 28):
            pkt = IP(dst=self.hostname, ttl=i) / UDP(dport=40000)
            reply = sr1(pkt, verbose=0, timeout=1)
            if reply is None or reply.type == 3:
                self.traceroute += "Done!\n"
                break
            else:
                self.traceroute += f'Hop {i}: {reply.src}\n'
        self.label.setText('' + self.traceroute)

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