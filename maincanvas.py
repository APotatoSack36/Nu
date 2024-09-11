from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

class MainCanvas:
    def __init__(self):
        self.width = 960
        self.height = 540
        self.label = QLabel()
        self.canvas = QPixmap(self.width, self.height)
        self.label.setPixmap(self.canvas)
        self.label.setMouseTracking(True)