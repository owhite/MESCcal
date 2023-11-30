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
            pb.clicked.connect(partial(self.buttonClicked, t['name'], le))

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

    def buttonClicked(self, name, line):
        n = line.text()
        if not self.port.isOpen():
            self.statusText.setText('Port closed: cant update')
        else:
            if self.is_int_or_float(n):
                text = 'set {0} {1}'.format(name, n)
                self.statusText.setText(text)
                text = text + '\r\n'
                self.parent.serialPayload.resetString() # do i need this?
                self.port.write( text.encode() )
                self.parent.serialPayload.resetTimer() # and this? 

            else:
                self.statusText.setText('{0} not number'.format(n))


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


    def getSerialData(self):
        self.statusText.setText('Serial: get')
        text = 'get\r\n'
        self.serialPayload.resetString()
        self.port.write( text.encode() )
        self.serialPayload.resetTimer()

    def saveSerialData(self):
        print("run save");

    def sine_wave_color_generator(self, frequency, amplitude, phase_shift):
        """
        Generate a sine wave and map it to a gradient of green colors.

        Parameters:
        - frequency: Frequency of the sine wave (default is 1).
        - amplitude: Amplitude of the sine wave (default is 1).
        - phase_shift: Phase shift of the sine wave (default is 0).

        Returns:
        - An HTML color string ranging from light green to dark green.
        """
        # Calculate the current time to introduce a time-dependent component
        current_time = time.time()
        # Calculate the angle based on the current time and parameters
        angle = (2 * math.pi * frequency * current_time) + phase_shift
        # Calculate the sine value and normalize it to the range [0, 1]
        value = (math.sin(angle) + 1) / 2
        # Apply amplitude
        value *= amplitude

        # Map the sine wave value to a gradient of green colors
        hue = 0.33  # Green hue
        saturation = 1.0
        lightness = value
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)

        # Convert RGB values to HTML color format
        html_color = "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))

        return html_color


    # a timer that checks if anything has recently been transmitted
    #  if it times out, then Jens term must have stopped
    #  so something like getSerialData() is not really the place
    #  to collected all the parsed information. 
    def checkSerialPayload(self):
        if not self.port.isDataTerminalReady(): # seems to indicate the port is dead
            self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            if self.serialWasOn:
                self.statusText.setText('Port died')
        else:
            html_color = self.sine_wave_color_generator(frequency=.4, amplitude=0.5, phase_shift=0)
            self.getButton.setStyleSheet(f'background-color: {html_color}; border: 1px solid green;')
            # self.getButton.setStyleSheet("background-color : #03AF00;" "border :1px solid green;")
            self.saveButton.setStyleSheet("background-color : #009900;" "border :1px solid green;") 
            self.serialWasOn = True

        if (self.serialPayload.reportTimer()) > 0.2:
            if len(self.serialPayload.reportString()) > 0:
                self.serialPayload.parsePayload()
                p = self.serialPayload.reportPayload()
                # if the payload has anything, try updating all the tabs
                if p is not None and len(p['names']) > 0:
                    for tab in self.tabs:
                        tab.updateValues(p)
                
                # now clear everything that was received
                self.serialPayload.resetTimer()
                self.serialPayload.resetString()
                

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mescal()
    window.show()
    app.exec()
