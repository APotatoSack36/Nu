from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QKeyEvent, QMouseEvent, QWheelEvent
import numpy

from maincanvas import MainCanvas
from entities import *

mouse_read = [0, 0]

lineArray = []
pointArray = []
linePointArray = []


class SketchWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.maincanvas = MainCanvas()
        self.maincanvas.canvas.fill(Qt.GlobalColor.black)

        self.setCentralWidget(self.maincanvas.label)
        self.tool = "line"
        self.mode = 0

        self.point_index = 0
        self.line_index = 0
        self.line_point_index = 0
        self.click_index = 0

        self.scaling_fac = 1.5
        self.zoom_str = 0
        self.total_str = 0

        self.delta_x = 0
        self.delta_y = 0

        self.delta_xa = [0]*21
        self.delta_ya = [0]*21

        self.global_point = Point(self.maincanvas)
        self.global_point.draw()

        self.app = app
        self.setWindowTitle("CAD")

        self.setMouseTracking(True)
        self.maincanvas.label.setPixmap(self.maincanvas.canvas)

    def keyPressEvent(self, event : QKeyEvent):
        if event.key() == 76:
            self.tool = "line"
        if event.key() == 80:
            self.tool = "point"
        if event.key() == 16777249:
            self.mode = "pan"

    def keyReleaseEvent(self, event : QKeyEvent):
        if event.key() == 16777249:
            self.mode = "NAN"


    def mouseMoveEvent(self, e):
        global mouse_read
        last_relative_mouse_pos = mouse_read
        mouse_read = self.relative_mouse_pos()
        if self.mode == "pan":
            self.transform((mouse_read[0] - last_relative_mouse_pos[0]), (mouse_read[1] - last_relative_mouse_pos[1]))
            self.delta_x += (mouse_read[0] - last_relative_mouse_pos[0])
            self.delta_y += (mouse_read[1] - last_relative_mouse_pos[1])
            self.delta_xa[self.total_str] = self.delta_x
            self.delta_ya[self.total_str] = self.delta_y
            print(self.delta_xa)


    def mousePressEvent(self, event : QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            match self.tool:
                case "point":
                    self.instatiate_point(self.relative_mouse_pos())
                case "line":
                    self.instatiate_line_point(self.relative_mouse_pos())
                    self.click_index += 1
                    if self.click_index >= 2:
                        self.instatiate_line()
                        self.click_index = 0

        if event.button() == Qt.MouseButton.MiddleButton:
            self.mode = "pan"
        if event.button() == Qt.MouseButton.RightButton:
            pass

    def mouseReleaseEvent(self, event : QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.mode = "NAN"

    def relative_mouse_pos(self):
        mouse = QCursor()
        windowPoint = self.pos()
        mousePoint = mouse.pos()
        relativeMouseX = mousePoint.x() - windowPoint.x()
        relativeMouseY = mousePoint.y() - windowPoint.y() - 32 #32 is the size of window bar

        return(relativeMouseX, relativeMouseY)

    def wheelEvent(self, event: QWheelEvent):
            if event.angleDelta().y() > 0  and self.total_str < 20: #Zoom in
                self.zoom_str = 1/self.scaling_fac
                self.total_str += 1
                self.scale(self.relative_mouse_pos())
            if event.angleDelta().y() < 0 and self.total_str > -20: #Zoom out
                self.zoom_str = self.scaling_fac
                self.total_str -= 1
                self.scale(self.relative_mouse_pos())

    def instatiate_point(self, point=[0,0]):
        pointArray.append(Point(self.maincanvas))
        pointArray[self.point_index].coordinates = [point[0] - self.delta_x, point[1] - self.delta_y, int(point[0]) -  self.delta_x, int(point[1]) - self.delta_y, point[0], point[1], int(point[0]), int(point[1])]
        pointArray[self.point_index].draw()
        self.point_index += 1

    def instatiate_line_point(self, point=[0,0]):
        linePointArray.append(Point(self.maincanvas))
        linePointArray[self.line_point_index].coordinates = [point[0] - self.delta_x, point[1] - self.delta_y, int(point[0] - self.delta_x), int(point[1] - self.delta_y), point[0], point[1], int(point[0]), int(point[1])]
        linePointArray[self.line_point_index].draw()
        self.line_point_index += 1

    def instatiate_line(self):
        lineArray.append(Line(self.maincanvas))
        lineArray[self.line_index].coordinates  =  [linePointArray[(self.line_index*2)].coordinates[0], linePointArray[(self.line_index*2)].coordinates[1], linePointArray[(self.line_index*2)+1].coordinates[0], linePointArray[(self.line_index*2)+1].coordinates[1],
                                                    linePointArray[(self.line_index*2)].coordinates[2], linePointArray[(self.line_index*2)].coordinates[3], linePointArray[(self.line_index*2)+1].coordinates[2], linePointArray[(self.line_index*2)+1].coordinates[3],
                                                    linePointArray[(self.line_index*2)].coordinates[4], linePointArray[(self.line_index*2)].coordinates[5], linePointArray[(self.line_index*2)+1].coordinates[4], linePointArray[(self.line_index*2)+1].coordinates[5],
                                                    linePointArray[(self.line_index*2)].coordinates[6], linePointArray[(self.line_index*2)].coordinates[7], linePointArray[(self.line_index*2)+1].coordinates[6], linePointArray[(self.line_index*2)+1].coordinates[7]]

        lineArray[self.line_index].draw()
        self.line_index += 1

    def scale(self, point=[0,0]):
        self.maincanvas.canvas.fill(Qt.GlobalColor.black)

        for v in range(0, len(pointArray)):
            pointArray[v].coordinates[4] = ((pointArray[v].coordinates[4] - point[0])/self.zoom_str) + point[0]
            pointArray[v].coordinates[5] = ((pointArray[v].coordinates[5] - point[1])/self.zoom_str) + point[1]
            pointArray[v].coordinates[6] = int(pointArray[v].coordinates[4])
            pointArray[v].coordinates[7] = int(pointArray[v].coordinates[5])
            pointArray[v].draw()

        for p in range(0, len(linePointArray)):
            linePointArray[p].coordinates[4] = ((linePointArray[p].coordinates[4] - point[0])/self.zoom_str) + point[0]
            linePointArray[p].coordinates[5] = ((linePointArray[p].coordinates[5] - point[1])/self.zoom_str) + point[1]
            linePointArray[p].coordinates[6] = int(linePointArray[p].coordinates[4])
            linePointArray[p].coordinates[7] = int(linePointArray[p].coordinates[5])
            linePointArray[p].draw()

        for g in range(0, len(lineArray)):
            lineArray[g].coordinates[8] = linePointArray[(g* 2)].coordinates[4]
            lineArray[g].coordinates[9] = linePointArray[(g* 2)].coordinates[5]
            lineArray[g].coordinates[10] = linePointArray[(g* 2) + 1].coordinates[4]
            lineArray[g].coordinates[11] = linePointArray[(g* 2) + 1].coordinates[5]
            lineArray[g].coordinates[12] = linePointArray[(g* 2)].coordinates[6]
            lineArray[g].coordinates[13] = linePointArray[(g* 2)].coordinates[7]
            lineArray[g].coordinates[14] = linePointArray[(g* 2) + 1].coordinates[6]
            lineArray[g].coordinates[15] = linePointArray[(g* 2) + 1].coordinates[7]
            lineArray[g].draw()

        self.global_point.coordinates[4] = ((self.global_point.coordinates[4] - point[0])/self.zoom_str) + point[0]
        self.global_point.coordinates[5] = ((self.global_point.coordinates[5] - point[1])/self.zoom_str) + point[1]
        self.global_point.coordinates[6] = int(self.global_point.coordinates[4])
        self.global_point.coordinates[7] = int(self.global_point.coordinates[5])
        self.global_point.draw()

    def transform(self, xspeed, yspeed):
        self.maincanvas.canvas.fill(Qt.GlobalColor.black)
 
        for k in range(0, len(pointArray)):
            pointArray[k].coordinates[4] += xspeed
            pointArray[k].coordinates[5] += yspeed
            pointArray[k].coordinates[6] += xspeed
            pointArray[k].coordinates[7] += yspeed
            pointArray[k].draw()

        for r in range(0, len(linePointArray)):
            linePointArray[r].coordinates[4] += xspeed
            linePointArray[r].coordinates[5] += yspeed
            linePointArray[r].coordinates[6] += xspeed
            linePointArray[r].coordinates[7] += yspeed
            linePointArray[r].draw()

        for b in range(0, len(lineArray)):
            lineArray[b].coordinates[8] = linePointArray[(b* 2)].coordinates[4]
            lineArray[b].coordinates[9] = linePointArray[(b* 2)].coordinates[5]
            lineArray[b].coordinates[10] = linePointArray[(b* 2) + 1].coordinates[4]
            lineArray[b].coordinates[11] = linePointArray[(b* 2) + 1].coordinates[5]
            lineArray[b].coordinates[12] = linePointArray[(b* 2)].coordinates[6]
            lineArray[b].coordinates[13] = linePointArray[(b* 2)].coordinates[7]
            lineArray[b].coordinates[14] = linePointArray[(b* 2) + 1].coordinates[6]
            lineArray[b].coordinates[15] = linePointArray[(b* 2) + 1].coordinates[7]
            lineArray[b].draw()

        self.global_point.coordinates[4] += xspeed
        self.global_point.coordinates[5] += yspeed
        self.global_point.coordinates[6] += xspeed
        self.global_point.coordinates[7] += yspeed
        self.global_point.draw()