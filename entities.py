from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
import math
from maincanvas import * 

class SketchEntity:
    def __init__(self, canvas):
        self.maincanvas = canvas
        self.lightGreen = QColor(145, 204, 145, 255)

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

    def draw_ghost(self, point=[0, 0]):
        self.painter = QPainter(self.maincanvas.canvas)
        self.pen = QPen()
        
        self.pen.setColor(Qt.GlobalColor.green)
        self.painter.setPen(self.pen)
        self.painter.drawEllipse(point[0] - 3, point[1] - 3, 6, 6)

        self.painter.end()
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)

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
        self.painter.drawLine(self.coordinates[4], self.coordinates[5], self.coordinates[6], self.coordinates[7])

        self.pen.setColor(Qt.GlobalColor.green)
        self.painter.setPen(self.pen)
        self.painter.drawLine(self.coordinates[12],self.coordinates[13], self.coordinates[14], self.coordinates[15])

        self.painter.end()
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)

    def draw_ghost(self, point1=[0, 0], point2=[0, 0]):
        self.painter = QPainter(self.maincanvas.canvas)
        self.pen = QPen()

        self.pen.setColor(Qt.GlobalColor.green)
        self.painter.setPen(self.pen)
        self.painter.drawLine(point1[0] ,point1[1], point2[0], point2[1])

        self.painter.end()
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)

class ThreePointArc(SketchEntity): #TBD
    def __init__(self, canvas):
        super().__init__(canvas)
        self.coordinates = [0, 0, 0, 0, 0, 0, #Basic
                            0, 0, 0, 0, 0, 0, #Basic Rounded
                            0, 0, 0, 0, 0, 0, #Transformed
                            0, 0, 0, 0, 0, 0] #Transformed rounded
        self.radius = 50
        self.angle = 0
        self.subdivides = 5
    
    def draw(self):
        self.painter = QPainter(self.maincanvas.canvas)
        self.pen = QPen()

        self.pen.setColor(Qt.GlobalColor.red)
        self.painter.setPen(self.pen)
        self.painter.drawLine(self.coordinates[6], self.coordinates[7], self.coordinates[10], self.coordinates[11])
        self.painter.drawLine(self.coordinates[8], self.coordinates[9], self.coordinates[10], self.coordinates[11])

        self.pen.setColor(Qt.GlobalColor.green)
        self.painter.setPen(self.pen)
        
        self.painter.drawLine(self.coordinates[18], self.coordinates[19], self.coordinates[22], self.coordinates[23])
        self.painter.drawLine(self.coordinates[20], self.coordinates[21], self.coordinates[22], self.coordinates[23])

        self.painter.end()
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)
    
    def draw_ghost(self, point1=[0, 0], point2=[0, 0], point3=[0, 0]):
        self.painter = QPainter(self.maincanvas.canvas)
        self.pen = QPen()

        self.pen.setColor(Qt.GlobalColor.green)
        self.painter.setPen(self.pen)
        self.painter.drawLine(point1[0] ,point1[1], point3[0], point3[1])
        self.painter.drawLine(point2[0] ,point2[1], point3[0], point3[1])

        self.painter.end()
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)