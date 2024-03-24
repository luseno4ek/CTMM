from PyQt6.QtCore import QObject, QThread, pyqtSignal
from ObjParser import *

class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, fe_model, path) -> None:
        super().__init__()
        self.fe_model = fe_model
        self.path = path

    def run(self):
        self.fe_model = ObjFileParser.parse_obj_to_finite_element_model(self.path, log_to_console=True)
        self.finished.emit()
