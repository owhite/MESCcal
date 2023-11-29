#!/usr/bin/env python3

import sys
import re
import math
import json
import Payload
import FirstTab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class createTab(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.tab_data = parent.tab_data[parent.tab_title]
        self.tab_title = parent.tab_title
        self.initUI()

    def initUI(self):
        self.setCentralWidget( QtWidgets.QWidget(self) )

        layout = QtWidgets.QFormLayout( self.centralWidget() )

        self.buttons =[]
        self.lineEdits =[]
        count = 0
        for value in self.tab_data['widgets']:
            pb = QtWidgets.QPushButton(value['value'])
            le = QtWidgets.QLineEdit()
            pb.clicked.connect(lambda checked, value=value: self.buttonClicked(value))

            layout.addRow(pb, le)
            count += 1

    def updateValues(self):
        print('Your name: ' + self.lineEdit1.text())

    def buttonClicked(self, n):
        print('Button {0} clicked. Contains'.format(n))


class Mescal(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mescal, self).__init__()

        ### Get a config file ### 
        file_path = "tab_contents.json"
        try:
            with open(file_path, 'r') as json_file:
                try:
                    self.tab_data = json.load(json_file)

                except json.JSONDecodeError as json_error:
                    print(f"Error decoding JSON: {json_error}")

        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")

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
        self.createStatusBar()

        ### Tabs ###
        self.tabWidget = QtWidgets.QTabWidget()
        self.tab_first = FirstTab.FirstTab(self)
        t = self.tabWidget.addTab(self.tab_first,"Port")
        # sets which tab to highlight
        # self.tabWidget.setCurrentIndex(t)

        self.tabs = []
        count = 0
        for t in self.tab_data.keys():
            self.tab_title = t
            tab = createTab(self)
            self.tabs.append(tab)
            self.tabWidget.addTab(tab,self.tab_data[t]['title'])
            count += 1

        self.setCentralWidget(self.tabWidget)

    def createStatusBar(self):
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


    def getSerialData(self):
        self.statusText.setText('Serial: get')
        text = 'get\r\n'
        self.serialPayload.resetString()
        self.port.write( text.encode() )
        self.serialPayload.resetTimer()

    def saveSerialData(self):
        struct = self.serialPayload.reportPayload()
        print("REPORTING");
        for l in struct['names']:
            print(l, struct[l]['value'])

    # a timer that checks if anything has recently been transmitted
    #  if it times out, then Jens term must have stopped
    #  so something like getSerialData() is not really the place
    #  to collected all the parsed information. 
    def checkSerialPayload(self):
        if (self.serialPayload.reportTimer()) > 0.2:
            if len(self.serialPayload.reportString()) > 0:
                self.serialPayload.parsePayload()
                self.serialPayload.resetTimer()
                self.serialPayload.resetString()
                

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mescal()
    window.show()
    app.exec()
