from PyQt5.QtWidgets import QApplication
import sys
import main_window

def main():
    window = main_window.Window()
    window.resize(575, 575)
    window.show()
    sys.exit(app.exec_())

app = QApplication(sys.argv)

if __name__ == '__main__':
    main()