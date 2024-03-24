import sys
from utils import *
from MainWindow import *
from PyQt6.QtWidgets import QApplication

# ------ BEGIN MAIN ------

# start application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

# ------ END MAIN ------
