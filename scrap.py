#!/usr/bin/env python3

import sys, json
import datetime
import time
import math
import colorsys

import ColorSegmentRing


from configparser import ConfigParser
import Payload, speedoPort, speedoPrefs
from keySound import keySound

import speedoObjects
import speedoThermo

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsItemGroup
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtGui import QPolygonF, QLinearGradient, QBrush

import qdarkgraystyle

import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class speedo(QtWidgets.QMainWindow):
    def __init__(self):
        super(speedo, self).__init__()

        self.min_width = 1920
        self.min_height = 1080

        ### Window ###
        self.setMinimumWidth(self.min_width)
        self.setMinimumHeight(self.min_height)
        self.tabWidget = QtWidgets.QTabWidget()

        ### create display tab here ###
        self.speedoTab = SpeedoTab(self)
        self.tabWidget.addTab(self.speedoTab, "speedo")

        self.setWindowTitle("speedo")
        self.setCentralWidget(self.tabWidget)


### Creates a tab that is described in a json config file
class SpeedoTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.min_width = parent.min_width
        self.min_height = parent.min_height
        self.max_amps = 20

        self.initUI()

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        self.graphics_view = QtWidgets.QGraphicsView(self)
        self.graphics_view.setMinimumSize(self.min_width, self.min_height)  # Set minimum size here
        scene = QtWidgets.QGraphicsScene(self)
        bck = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(0, 0), QtCore.QPointF(self.min_width, 0),
                                              QtCore.QPointF(self.min_width, self.min_height),
                                              QtCore.QPointF(0, self.min_height), QtCore.QPointF(0, 0)]))
        bck.setBrush(QtGui.QColor(QtCore.Qt.black))
        scene.addItem(bck)

        self.adc1_ring = ColorSegmentRing.colorSegmentRing()
        self.adc1_ring.setVisible(True)
        self.adc1_ring.ring_text = 'adc1'
        self.adc1_ring.ring_text_size = 12
        scene.addWidget(self.adc1_ring)

        self.graphics_view.setScene(scene)
        main_layout.addWidget(self.graphics_view)
        self.setWindowTitle('Polygon Coloring App with QLCDNumber')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = speedo()
    window.show()
    app.exec()
