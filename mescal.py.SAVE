#!/usr/bin/env python3

import sys
import re
import math
import time
import colorsys
import json
import Payload
import FirstTab
from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

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
        self.timer.timeout.connect(self.checkSerialStatus) # monitors if json is coming in
        self.timer.start(50)
        self.serialStreamingOn = False
        self.serialWasOn = False
        self.serialButtonInc = 9
        self.serialButtonColor = ''
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

        self.streamButton = QtWidgets.QPushButton("D") # D for data
        self.streamButton.setStyleSheet("background-color : white;" "border :2px solid white;") 
        self.streamButton.setFixedSize(30, 32)
        self.streamButton.setCheckable(True)
        self.streamButton.clicked.connect(self.getSerialStream)
        self.statusBar().addWidget( self.streamButton)

    def serialButtonOff(self):
        self.streamButton.setStyleSheet("background-color : white;" "border :2px solid black;") 
        self.streamButton.setChecked(True)
        self.serialStreamingOn = False

    def serialButtonOn(self):
        self.streamButton.setStyleSheet("background-color : white;" "border :2px solid blue;") 
        self.streamButton.setChecked(False)
        self.serialStreamingOn = True

    def getSerialStream(self, checked):
        if checked: # then stop things
            self.statusText.setText('Serial: no streaming')
            text = 'status stop\r\n'
        else:
            self.statusText.setText('Serial: streaming')
            text = 'status json\r\n'
            self.serialPayload.resetTimer()

        self.port.write( text.encode() )

    def getSerialData(self):
        self.statusText.setText('Serial: get')
        text = 'get\r\n'
        self.port.write( text.encode() )

    def saveSerialData(self):
        print("run save");

    # colors to make get button throb
    def buttonColorGenerator(self, frequency, amplitude, phase_shift):
        current_time = time.time()
        angle = (2 * math.pi * frequency * current_time) + phase_shift
        value = (math.sin(angle) + 1) / 2
        value *= amplitude
        hue = 0.33  # Green hue
        saturation = 1.0
        lightness = value
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        html_color = "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))
        return html_color

    # this gets a string that may have commands in it
    def updateTabs(self):
        if len(self.serialPayload.reportString()) > 0:
            self.serialPayload.parsePayload()
            p = self.serialPayload.reportPayload()
            # update tabs if the payload has anything, 
            if p is not None and len(p['names']) > 0:
                for tab in self.tabs:
                    tab.updateValues(p)

        self.serialPayload.resetString()


    # a timer that checks if anything has recently been transmitted
    def checkSerialStatus(self):
        if not self.port.isDataTerminalReady(): # seems to indicate the port is dead
            self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            if self.serialWasOn:
                self.statusText.setText('Port died')
        else:
            html_color = self.buttonColorGenerator(frequency=.4, amplitude=0.5, phase_shift=0)
            self.getButton.setStyleSheet(f'background-color: {html_color}; border: 1px solid green;')
            self.saveButton.setStyleSheet("background-color : #009900;" "border :1px solid green;") 
            self.serialWasOn = True

        if (self.serialPayload.reportTimer()) > 0.2: # checks if json is coming in
            self.serialButtonOff()
        else:
            self.serialButtonOn()
                
class createTab(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.port = parent.port
        self.tab_data = parent.tab_data[parent.tab_title]
        self.tab_title = parent.tab_title
        self.statusText = parent.statusText
        self.initUI()

    def initUI(self):
        self.setCentralWidget( QtWidgets.QWidget(self) )

        layout = QtWidgets.QFormLayout( self.centralWidget() )

        self.buttons =[]
        self.lineEdits ={}
        count = 0
        for t in self.tab_data['widgets']:
            pb = QtWidgets.QPushButton(t['name'])
            le = QtWidgets.QLineEdit()
            self.lineEdits[t['name']] = le
            pb.clicked.connect(partial(self.dataEntryButtonClicked, t['name'], le))

            layout.addRow(pb, le)
            count += 1

    def updateValues(self, struct):
        for w in self.tab_data['widgets']:
            n = w['name']
            r = struct.get(n)
            if r:
                self.lineEdits[n].setText(r['value'])

    def is_int_or_float(self, s):
        try:
            int_value = int(s)
            return True
        except ValueError:
            try:
                float_value = float(s)
                return True
            except ValueError:
                return False

    def dataEntryButtonClicked(self, name, line):
        n = line.text()
        if not self.port.isOpen():
            self.statusText.setText('Port closed: cant update')
        else:
            if self.is_int_or_float(n):
                text = 'set {0} {1}'.format(name, n)
                self.statusText.setText(text)
                text = text + '\r\n'
                self.port.write( text.encode() )
                # self.parent.serialPayload.resetString() # 

            else:
                self.statusText.setText('{0} not number'.format(n))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mescal()
    window.show()
    app.exec()
