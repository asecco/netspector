from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QCheckBox, QMessageBox, QShortcut
from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage, QKeySequence
from PyQt5.QtCore import Qt
import qdarktheme
import sys
import requests
import pprint
import re
import os
import time
import configparser
from scapy.layers.inet import IP, sr1, UDP
import main
import log_window
import dns_lookup_window

class Window(QMainWindow):
    ip_dict = {}
    owd = os.getcwd()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetSpector")
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

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setMinimumHeight(200)
        self.layout.addWidget(self.scroll_area)

        self.map_label = QLabel()
        self.map_label.setHidden(True)
        self.map_label.setMaximumHeight(400)
        self.layout.addWidget(self.map_label, stretch=1)
        self.layout.setAlignment(self.map_label, Qt.AlignCenter)

        self.dt_checkbox = QCheckBox('Dark Theme')
        self.dt_checkbox.stateChanged.connect(self.checkbox_click)
        self.layout.addWidget(self.dt_checkbox)
        self.layout.setAlignment(self.dt_checkbox, Qt.AlignLeft)

        self.shortcut = QShortcut(QKeySequence("RETURN"), self)
        self.shortcut.activated.connect(self.lookup_btn_click)

        self.create_config()
        self.read_config()
    
    def create_menu(self):
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu("File")
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.about_btn_click)
        self.file_menu.addAction(self.about_action)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.exit_btn_click)
        self.file_menu.addAction(self.exit_action)

        self.tools_menu = self.menubar.addMenu("Tools")
        self.dns_action = QAction("DNS Lookup", self)
        self.dns_action.triggered.connect(self.dns_btn_click)
        self.tools_menu.addAction(self.dns_action)

        self.logs_action = QAction("IP Logs", self)
        self.logs_action.triggered.connect(self.logs_btn_click)
        self.tools_menu.addAction(self.logs_action)
    
    def lookup_btn_click(self):
        self.textbox_value = self.textbox.text().strip()
        self.request = requests.get(f"http://ip-api.com/json/{self.textbox_value}?fields=country,regionName,city,zip,isp,proxy,message,lat,lon").json()
        self.request = pprint.pformat(self.request, sort_dicts=False).replace('{', '').replace('}', '').replace("'", '')

        if self.textbox_value != '' and self.request != 'message: invalid query':
            self.ip_dict[self.textbox_value] = str(self.request)
        
        if self.request != 'message: invalid query' and self.request != 'message: private range':
            self.label.setText(' ' + str(self.request))
            self.map_label.setStyleSheet("border: 2px solid black;")
            self.label.setHidden(False)
            self.map_coordinates(self.request)
            self.map_label.setHidden(False)
            self.textbox.setStyleSheet("")
        else:
            self.map_label.setHidden(True)
            self.label.setHidden(True)
            self.textbox.setStyleSheet("border: 2px solid red;")
            QMessageBox.critical(self, "Error", "Invalid IP!")
    
    def map_coordinates(self, r):
        self.lat = re.search(r'lat:\s(.*)', r).group().replace('lat: ', '')
        self.lon = re.search(r'lon:\s(.*)', r).group().replace('lon: ', '')

        self.map_url = f"https://cache.ip-api.com/{self.lon}{self.lat}10"
        self.map = QImage()
        self.map.loadFromData(requests.get(self.map_url).content)
        self.map_label.setPixmap(QPixmap(self.map))
    
    def traceroute_btn_click(self):
        try:
            self.hostname = self.textbox.text().strip()
            self.traceroute = ''
            self.map_label.setHidden(True)
            self.label.setHidden(False)
            self.label.setText('Traceroute started. Please wait...')
            self.label.repaint()
            self.textbox.setStyleSheet("")
            self.textbox.repaint()
            
            consecutive_no_response = 0
            completed = False
            for i in range(1, 28):
                packet = IP(dst=self.hostname, ttl=i) / UDP(dport=33434)
                start_time = time.time()
                reply = sr1(packet, verbose=0, timeout=2)
                end_time = time.time()
                if reply is None:
                    consecutive_no_response += 1
                    if consecutive_no_response > 3:
                        self.traceroute += f'More than {3} consecutive no-response hops\n'
                        self.label.setText(self.traceroute)
                        self.label.repaint()
                        break
                    self.traceroute += f'Hop {i}: No response\n'
                    self.label.setText(self.traceroute)
                    self.label.repaint()
                elif reply.type == 3:
                    self.traceroute += "Traceroute complete\n"
                    self.label.setText(self.traceroute)
                    completed = True
                    break
                else:
                    latency = (end_time - start_time) * 1000
                    consecutive_no_response = 0
                    request = requests.get(f"http://ip-api.com/json/{reply.src}?fields=city,country,isp").json()
                    city = request.get("city")
                    country = request.get("country")
                    isp = request.get("isp")
                    if city and country and isp:
                        self.traceroute += f'Hop {i}: {reply.src} - {city}, {country}, {isp} - ({latency:.2f} ms)\n'
                        self.label.setText(self.traceroute)
                        self.label.repaint()
                    else:
                        self.traceroute += f'Hop {i}: {reply.src} - ({latency:.2f} ms)\n'
                        self.label.setText(self.traceroute)
                        self.label.repaint()
            
            if not completed:
                self.traceroute += "Traceroute ended\n"
                self.label.setText(self.traceroute)
        except:
            self.textbox.setStyleSheet("border: 2px solid red;")
            QMessageBox.critical(self, "Error", "Invalid IP!")
            self.label.setText('')

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
    
    def dns_btn_click(self):
        self.dns_lookup_window = dns_lookup_window.DNSLookupWindow()
        self.dns_lookup_window.resize(400, 300)
        self.dns_lookup_window.show()

    def logs_btn_click(self):
        self.log_window = log_window.LogWindow()
        self.log_window.resize(400, 300)
        self.log_window.show()

    def about_btn_click(self):
        QMessageBox.about(self, "About", "Created By: Andrew Secco\n\nhttps://github.com/asecco")

    def exit_btn_click(self):
        sys.exit()