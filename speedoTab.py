#!/usr/bin/env python3

import re
import sys
import speedoObjects
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTabWidget, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QLinearGradient, QBrush
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import QTimer

### Creates a tab that is described in a json config file
class SpeedoTab(QtWidgets.QWidget):  # Use QWidget instead of QMainWindow
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # self.port = parent.port
        self.initUI()

    def initUI(self):
        self.spd = speedoObjects.SpeedoData().spd
        self.speedDigits = []
        self.maxSpeed = 55

        main_layout = QtWidgets.QVBoxLayout(self)

        # Create a QGraphicsView and a QGraphicsScene
        graphics_view = QGraphicsView(self)
        scene = QGraphicsScene(self)


        bck = QGraphicsPolygonItem(QPolygonF([QPointF(0, 0), QPointF(600, 0), QPointF(600, 480), QPointF(0, 480), QPointF(0, 0)]))
        bck.setBrush(QColor(Qt.black))
        scene.addItem(bck)

        font = QFont("Futura", 40, QFont.Medium, italic=True)
        for x, pos in enumerate(speedoObjects.SpeedoData().speedDigits):
            t = QGraphicsTextItem(str(x * 10))
            t.setFont(font)
            t.setDefaultTextColor(QColor(Qt.black))
            x = t.boundingRect().center().x()
            y = t.boundingRect().center().y()
            t.setPos(pos[0]-x, pos[1]-y)
            scene.addItem(t)
            self.speedDigits.append(t)

        polygon = QPolygonF([QPointF(0, 0), QPointF(100, 0), QPointF(50, 100)])

        # Create a QGraphicsPolygonItem
        item = QGraphicsPolygonItem(polygon)
        gradient = QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0, QColor(255, 0, 0))  # Starting color
        gradient.setColorAt(1, QColor(0, 0, 0, 0)) 
        # Set the brush with the gradient
        brush = QBrush(gradient)
        item.setBrush(brush)
        scene.addItem(item)

        self.speedObjs = []
        for array in self.spd:
            l = []
            for (x,y) in array:
                l.append(QPointF(x, y))
                item = QPolygonF(l)
            item = QGraphicsPolygonItem(item)
            item.setBrush(QColor(Qt.white))
            scene.addItem(item)
            self.speedObjs.append(item)

        graphics_view.setScene(scene)

        amps_text = QGraphicsTextItem("110")
        font = QFont("Futura", 150, QFont.Medium, italic=True)
        amps_text.setFont(font)
        amps_text.setDefaultTextColor(QColor(Qt.white))
        x = amps_text.boundingRect().center().x()
        y = amps_text.boundingRect().center().y()
        amps_text.setPos(300 - x, 240 - y)
        scene.addItem(amps_text)

        amp_title = QGraphicsTextItem("Amps")
        font = QFont("Futura", 50, QFont.Medium, italic=True)
        amp_title.setFont(font)
        amp_title.setDefaultTextColor(QColor(Qt.black))
        amp_title.setPos(300, 240 + (amps_text.boundingRect().center().y() / 2))
        scene.addItem(amp_title)

        self.updateSpeedObjs(21)

        main_layout.addWidget(graphics_view)
        self.setWindowTitle('Polygon Coloring App with QLCDNumber')

    def updateSpeedObjs(self, speed):
        length = len(self.speedObjs) - 1

        if speed < 0: speed = 0
        if speed > self.maxSpeed: speed = self.maxSpeed

        x = int(speed / 10)
        for i, t in enumerate(self.speedDigits):
            if i <= x:
                t.setDefaultTextColor(QColor(Qt.red))
            else:
                t.setDefaultTextColor(QColor(Qt.white))

        pos = int((speed / self.maxSpeed) * length) + 1
        for i in range(pos):
            self.speedObjs[i].setBrush(QColor(Qt.red))

    def updateValuesWithGet(self, struct):
        print("received big struct from get")

    def updateValuesWithStream(self, struct):
        self.lcd_number1.display(struct['ehz'])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 632, 520)  # Set window dimensions
        self.central_widget = SpeedoTab(self)
        self.setCentralWidget(self.central_widget)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())        
