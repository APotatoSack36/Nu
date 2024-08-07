import sys
from PyQt6.QtWidgets import QApplication
from mainwindow import SketchWindow

app = QApplication(sys.argv)

window = SketchWindow(app)
window.show()
app.exec()