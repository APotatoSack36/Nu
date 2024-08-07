from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from maincanvas import * 

class SketchEntity:
    def __init__(self, canvas):
        self.maincanvas = canvas
        self.lightGreen = QColor(145, 204, 145, 255)

class Line(SketchEntity):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.coordinates = [0, 0, 0, 0, #Basic
                            0, 0, 0, 0, #Basic Rounded
                            0, 0, 0, 0, #Transformed
                            0, 0, 0, 0] #Transformed Rounded
    def draw(self):
        self.painter = QPainter(self.maincanvas.canvas)
        self.pen = QPen()

        #MAIN LINE
        self.pen.setColor(Qt.GlobalColor.red)
        self.painter.setPen(self.pen)
        self.painter.drawLine(self.coordinates[4],self.coordinates[5], self.coordinates[6], self.coordinates[7])

        self.pen.setColor(self.lightGreen)
        self.painter.setPen(self.pen)
        self.painter.drawLine(self.coordinates[12],self.coordinates[13], self.coordinates[14], self.coordinates[15])

        self.painter.end()
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)

class Point(SketchEntity):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.coordinates = [0, 0, #Basic
                            0, 0, #Basic Rounded
                            0, 0, #Transformed
                            0, 0] #Transformed rounded

    def draw(self):
        self.painter = QPainter(self.maincanvas.canvas)
        self.pen = QPen()

        self.pen.setColor(Qt.GlobalColor.red)
        self.painter.setPen(self.pen)
        self.painter.drawEllipse(self.coordinates[2] - 3, self.coordinates[3] - 3, 6, 6)

        self.pen.setColor(Qt.GlobalColor.lightGray)
        self.painter.setPen(self.pen)
        self.painter.drawEllipse(self.coordinates[6] - 3, self.coordinates[7] - 3, 6, 6)

        self.painter.end()
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)