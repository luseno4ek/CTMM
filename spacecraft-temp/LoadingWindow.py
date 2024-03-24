from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout
)
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QSize

class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint) 

        self.label_loading = QLabel("Loading...")
        self.movie = QMovie('images\loading.gif')
        self.movie.setScaledSize(QSize(200,200))

        self.label_loading.setMovie(self.movie)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label_loading,1,1)
        self.setLayout(self.grid)

        self.start_animation()
        self.setWindowTitle("Loading...")
        self.show()
    
    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
        self.close()