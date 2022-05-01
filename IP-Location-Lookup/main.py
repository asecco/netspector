from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarktheme
import requests
import sys
import pprint
import re

class Window(QMainWindow):
    ip_list = []
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Location Lookup")
        self.setFixedSize(650, 500)
        self.setWindowIcon(QIcon('IP-Location-Lookup/img/icon.ico'))
        app.setStyleSheet(qdarktheme.load_stylesheet("light"))

        self.init_ui()
        self.show()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("About", self.about_button)
        file_menu.addAction("Exit", self.exit_button)

        file_menu = menubar.addMenu("Tools")
        file_menu.addAction("IP Logs", self.logs_button)

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("69.89.31.226")
        self.textbox.move(60, 30)
        self.textbox.resize(400, 35)

        self.button = QPushButton("Lookup", self)
        self.button.setFont(QFont('Arial', 11))
        self.button.move(470, 30)
        self.button.resize(115, 35)
        self.button.clicked.connect(self.button_click)

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

    def button_click(self):
        self.textbox_value = self.textbox.text().strip()
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
            app.setStyleSheet(qdarktheme.load_stylesheet())
        else:
            app.setStyleSheet(qdarktheme.load_stylesheet("light"))

    def enter_shortcut(self):
        self.button.click()

    def logs_button(self):
        self.history_window = HistoryWindow()
        self.history_window.show()

    def about_button(self):
        QMessageBox.about(self, "About", "Created By: Andrew Secco\n\nhttps://github.com/asecco")

    def exit_button(self):
        sys.exit()

class HistoryWindow(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("IP Logs")
        self.setFixedSize(350, 200)
        self.setWindowIcon(QIcon('IP-Location-Lookup/img/icon.ico'))

        self.ips = Window.ip_list
        self.addItems(self.ips)

        self.clear_btn = QPushButton('Clear', self)
        self.clear_btn.setFont(QFont('Arial', 11))
        self.clear_btn.move(295, 170)
        self.clear_btn.resize(50, 25)
        self.clear_btn.clicked.connect(self.clear_click)

    def clear_click(self):
        self.clear()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())