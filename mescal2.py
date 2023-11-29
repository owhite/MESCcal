#!/usr/bin/env python3

import sys
import re
import math
# from Payload import Payload
import Payload
import FirstTab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class Mescal(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mescal, self).__init__()

        ### Window ### 
        self.move(QApplication.desktop().availableGeometry().bottomLeft())
        self.setMinimumWidth(800)
        self.setMinimumHeight(300)

        ### Serial stuff ###
        self.port = QSerialPort()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkSerialPayload)
        self.timer.start(50)

        self.serialPayload = Payload.Payload()
        self.serialPayload.startTimer()

        ### Status Bar ###
        self.setStatusBar( QtWidgets.QStatusBar(self) )

        self.statusText = QtWidgets.QLabel(self)
        self.statusText.setAlignment(QtCore.Qt.AlignRight)
        self.statusText.setText('Port closed')
        self.statusBar().addPermanentWidget( self.statusText )

        self.getButton = QtWidgets.QPushButton("G")
        self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid black;") 
        self.getButton.setFixedSize(30, 32)
        self.getButton.clicked.connect(self.getSerialData)
        self.statusBar().addWidget( self.getButton )

        self.saveButton = QtWidgets.QPushButton("S")
        self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid black;") 
        self.saveButton.setFixedSize(30, 32)
        self.saveButton.clicked.connect(self.saveSerialData)
        self.statusBar().addWidget( self.saveButton)

        ### Tabs ###
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)

        self.tab_first = FirstTab.FirstTab(self)
        t = self.tabWidget.addTab(self.tab_first,"Port")
        self.tab_second = SecondTab(self)
        self.tabWidget.addTab(self.tab_second,"Motor parameters")

        # sets which tab to highlight
        self.tabWidget.setCurrentIndex(t)

    # a timer that checks if anything has recently been transmitted
    #  if it times out, then Jens term must have stopped
    def checkSerialPayload(self):
        if (self.serialPayload.reportTimer()) > 0.2:
            if len(self.serialPayload.reportString()) > 0:
                self.serialPayload.parsePayload()
                self.serialPayload.resetTimer()
                self.serialPayload.resetString()
                
    def getSerialData(self):
        self.statusText.setText('Serial: get')
        text = 'get\r\n'
        self.serialPayload.resetString()
        self.port.write( text.encode() )
        self.serialPayload.resetTimer()
        print ("here")

    def saveSerialData(self):
        print("s");
        

class SecondTab(QtWidgets.QMainWindow): # motor parameters

    def __init__(self, parent):
        super().__init__(parent)
        self.port = parent.port
        self.statusText = parent.statusText
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
