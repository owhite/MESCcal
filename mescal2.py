#!/usr/bin/env python3

# https://ymt-lab.com/en/post/2021/pyqt5-serial-monitor/

import sys
import math
import FirstTab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class Mescal(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mescal, self).__init__()

        self.port = QSerialPort()

        self.setMinimumWidth(800)
        self.setMinimumHeight(300)

        self.tabWidget = QtWidgets.QTabWidget()
        # sets the tabWidget as the central widget inside the QMainWindow
        self.setCentralWidget(self.tabWidget)

        ### Status Bar ###
        self.setStatusBar( QtWidgets.QStatusBar(self) )
        self.statusText = QtWidgets.QLabel(self)
        self.statusBar().addWidget( self.statusText )
        
        ### Tabs ###

        self.tab_first = FirstTab.FirstTab(self.port, self.statusText)
        self.tabWidget.addTab(self.tab_first,"Port")
        self.tab_second = SecondTab(self.port, self.statusText)
        self.tabWidget.addTab(self.tab_second,"Motor parameters")


class SecondTab(QtWidgets.QMainWindow): # motor parameters

    def __init__(self, port, statusText):
        super().__init__()
        self.port = port
        self.statusText = statusText
        self.initUI()

    def initUI(self):

        self.setCentralWidget( QtWidgets.QWidget(self) )

        layout = QtWidgets.QFormLayout( self.centralWidget() )

        self.pb1 = QtWidgets.QPushButton("One")
        self.lineEdit1 = QtWidgets.QLineEdit()
        self.pb2 = QtWidgets.QPushButton("Two")
        self.lineEdit2 = QtWidgets.QLineEdit()
        self.pb3 = QtWidgets.QPushButton("Three")
        self.lineEdit3 = QtWidgets.QLineEdit()

        layout.addRow(self.pb1, self.lineEdit1)
        layout.addRow(self.pb2, self.lineEdit2)
        layout.addRow(self.pb3, self.lineEdit3)

        self.pb1.clicked.connect(self.pb1Clicked)

    def pb1Clicked(self):
        print('Your name: ' + self.lineEdit1.text())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mescal()
    window.show()
    app.exec()
