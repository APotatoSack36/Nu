from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

class MainCanvas:
    def __init__(self):
        self.label = QLabel()
        self.canvas = QPixmap(1000, 800)
        self.label.setPixmap(self.canvas)
        self.label.setMouseTracking(True)