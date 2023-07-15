from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import socket

class DNSLookupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DNS Lookup")
        self.setWindowIcon(QIcon('icon.ico'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.form_layout = QFormLayout()
        self.textbox = QLineEdit()
        self.textbox.setPlaceholderText("google.com")
        self.form_layout.addRow("Domain:", self.textbox)

        self.lookup_btn = QPushButton("Lookup")
        self.lookup_btn.setFont(QFont('Arial', 11))
        self.lookup_btn.clicked.connect(self.dns_lookup_btn_click)

        self.form_layout.addRow("", self.lookup_btn)
        self.layout.addLayout(self.form_layout)

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setFont(QFont('Arial', 11))
        self.label.setMinimumHeight(200)
        self.label.setAlignment(Qt.AlignTop)
        self.label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_context_menu)


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setMinimumHeight(200)
        self.layout.addWidget(self.scroll_area)

        self.shortcut = QShortcut(QKeySequence("RETURN"), self)
        self.shortcut.activated.connect(self.dns_lookup_btn_click)

        self.ip_address = None

    def dns_lookup_btn_click(self):
        self.domain = self.textbox.text().strip()
        self.hostname, self.ip = self.get_dns_info(self.domain)
        self.display_result(self.hostname, self.ip)

    def get_dns_info(self, domain):
        try:
            return socket.gethostbyname_ex(domain)[0:1] + socket.gethostbyname_ex(domain)[2:]
        except socket.gaierror:
            QMessageBox.critical(self, "Error", "Invalid domain!")
            return None, None

    def display_result(self, hostname, ip):
        self.result_text = ""
        if hostname:
            self.result_text += f"Hostname: {hostname}\n"
        if ip:
            self.result_text += f"IP Addresses: {', '.join(ip)}\n"
            self.ip_address = ip[0]
        self.label.setText(self.result_text)

    def show_context_menu(self):
        self.context_menu = QMenu(self)
        self.copy_action = QAction("Copy IP", self)
        self.copy_action.triggered.connect(self.copy_ip_address)
        self.context_menu.addAction(self.copy_action)
        self.context_menu.exec_(QCursor.pos())

    def copy_ip_address(self):
        if self.ip_address:
            self.clipboard = QApplication.clipboard()
            self.clipboard.setText(self.ip_address)
            QMessageBox.information(self, "Copy IP", f"IP address {self.ip_address} copied!")