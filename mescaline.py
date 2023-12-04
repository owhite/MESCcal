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
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QGroupBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class Mescaline(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mescaline, self).__init__()

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
        self.prevStatusText = ''

        ### Tabs ###
        self.tabWidget = QtWidgets.QTabWidget()
        self.tab_first = FirstTab.FirstTab(self)
        self.tabWidget.addTab(self.tab_first,"PORT")

        self.tabs = []
        count = 0
        for t in self.tab_data.keys():
            self.tab_dict = self.tab_data[t]
            self.boxes = self.tab_data[t]['boxes']
            tab = createTab(self)
            self.tabs.append(tab)
            self.tabWidget.addTab(tab,self.tab_data[t]['title'])

        # self.tabWidget.setCurrentIndex(p)

        self.setWindowTitle("Mescaline")
        self.setCentralWidget(self.tabWidget)

    def createStatusBar(self):
        status_bar = QtWidgets.QStatusBar(self)

        self.setStatusBar( status_bar )
        self.statusText = QtWidgets.QLabel(self)
        self.statusText.setAlignment(QtCore.Qt.AlignRight)
        self.statusText.setText('Status msgs here')
        self.statusBar().addPermanentWidget( self.statusText )

        # Create a widget to hold the layout
        self.layout_widget = QtWidgets.QWidget(self)

        # Create a horizontal layout for the widget
        layout = QtWidgets.QHBoxLayout(self.layout_widget)

        # Create buttons
        self.getButton = QtWidgets.QPushButton("G")
        self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid black;") 
        self.getButton.setFixedSize(30, 32)
        self.getButton.clicked.connect(self.getSerialData)
        self.getButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Get: retreive values from MESC, load into tabs")
        self.getButton.leaveEvent = self.customButtonHoverLeave

        self.saveButton = QtWidgets.QPushButton("S")
        self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid black;") 
        self.saveButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Save: store all values in MESC")
        self.saveButton.leaveEvent = self.customButtonHoverLeave
        self.saveButton.setFixedSize(30, 32)
        self.saveButton.clicked.connect(self.saveSerialData)

        self.streamButton = QtWidgets.QPushButton("D") # D for data
        self.streamButton.setStyleSheet("background-color : white;" "border :2px solid white;") 
        self.streamButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Data: toggles data streaming from MESC")
        self.streamButton.leaveEvent = self.customButtonHoverLeave
        self.streamButton.setFixedSize(30, 32)
        self.streamButton.setCheckable(True)
        self.streamButton.clicked.connect(self.getSerialStream)

        # Add buttons and status label to the layout
        layout.addWidget(self.getButton)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.streamButton)

        # Create a label for Vbus
        self.vbusText = QtWidgets.QLabel('Vbus:\n  ')
        layout.addWidget(self.vbusText)

        # Create a label for PhaseA
        self.phaseAText = QtWidgets.QLabel('PhaseA:\n  ')
        w = layout.addWidget(self.phaseAText)

        # Create a label for the status text
        # self.statusText = QtWidgets.QLabel('Status msgs here')

        # Set the widget containing the layout as the central widget of the status bar
        status_bar.addWidget(self.layout_widget)

    def customButtonHoverEnter(self, event, message):
        self.prevStatusText = self.statusText.text()
        self.statusText.setText(message)

    def customButtonHoverLeave(self, event):
        # I didnt like hos this behave, just clear the text
        # self.statusText.setText(self.prevStatusText)
        self.statusText.setText('Status msgs here')

    def serialButtonOff(self):
        self.streamButton.setStyleSheet("background-color : white;" "border :2px solid black;") 
        self.streamButton.setChecked(True)
        self.serialStreamingOn = False

    def serialButtonOn(self):
        html_color = self.buttonColorGenerator(frequency=.4, amplitude=0.5, phase_shift=0, hue = 0.77) # Green hue = 0.33
        self.streamButton.setStyleSheet(f'background-color: {html_color}; border: 1px solid green;')
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
        self.statusText.setText('CMD: get')
        text = 'get\r\n'
        self.port.write( text.encode() )

    def saveSerialData(self):
        self.statusText.setText('CMD: save')
        text = 'save\r\n'
        self.port.write( text.encode() )

    def updateJsonData(self, str):
        str = str.rstrip('\n')
        for row in str.split('\n'):
            try:
                self.streamDict = json.loads(row)
                self.updateStatusJson(self.streamDict)
            except json.JSONDecodeError as e:
                print("Getting bad json: {0}".format(row))

    def updateStatusJson(self, streamDict):
        f = round(streamDict['vbus'], 1)
        self.vbusText.setText('Vbus:\n{0}'.format(f))

        f = math.sqrt((streamDict['iq'] * streamDict['iq']) + (streamDict['id'] * streamDict['id']))
        f = round(f, 1)
        self.phaseAText.setText('PhaseA:\n{0}'.format(f))

    # most of the tabs have values loaded from the mesc payload
    #  this handles updating those values
    def updateTabs(self):
        if len(self.serialPayload.reportString()) > 0:
            self.serialPayload.parsePayload()
            p = self.serialPayload.reportPayload()
            # update tabs if the payload has anything, 
            if p is not None and len(p['names']) > 0:
                for tab in self.tabs:
                    tab.updateValues(p)

        self.serialPayload.resetString()

    # colors to make get button throb
    def buttonColorGenerator(self, frequency, amplitude, phase_shift, hue):
        current_time = time.time()
        angle = (2 * math.pi * frequency * current_time) + phase_shift
        value = (math.sin(angle) + 1) / 2
        value *= amplitude
        saturation = 1.0
        lightness = value
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        html_color = "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))
        return html_color

    # a timer that checks if anything has recently been transmitted
    def checkSerialStatus(self):
        if not self.port.isDataTerminalReady(): # seems to indicate the port is dead
            self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            if self.serialWasOn:
                self.statusText.setText('Port died')
        else:
            html_color = self.buttonColorGenerator(frequency=.4, amplitude=0.5, phase_shift=0, hue = 0.33) # Green hue = 0.33
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
        self.tab_dict = parent.tab_dict
        self.boxes = self.tab_dict['boxes']
        self.tab_title = self.tab_dict['title']
        self.port = parent.port
        self.statusText = parent.statusText
        self.initUI()

    def initUI(self):
        self.buttons =[]
        self.entryItem ={}

        self.setCentralWidget( QtWidgets.QWidget(self) )
        tab_layout = QtWidgets.QFormLayout( self.centralWidget() )

        for box in self.boxes:
            button_rows = box['buttons']
            tab_layout.addWidget(self.createBox(box['name'], button_rows))

    def createBox(self, box_name, button_rows):
        group_box = QtWidgets.QGroupBox(box_name)
        group_box_layout = QtWidgets.QVBoxLayout()
        for row in button_rows:
            group_box_layout.addLayout(self.createRow(row))

        group_box.setLayout(group_box_layout)

        return(group_box)

    def createRow(self, row):
        # Create a row with QHBoxLayout
        row_layout = QtWidgets.QHBoxLayout()
        row_layout.setSpacing(0)

        for buttons in row:

            if "comboBox" in buttons['type']:
                entry_item = QtWidgets.QComboBox()
                entry_item.addItem('none')
                for i in buttons['list']:
                    entry_item.addItem(i)
            else:
                entry_item = QtWidgets.QLineEdit()
                
            pb = QtWidgets.QPushButton(buttons['name'])
            self.entryItem[buttons['name']] = entry_item
            entry_item.setFixedWidth(100)
            pb.setFixedWidth(120)
            pb.setToolTip(buttons['desc'])
            pb.clicked.connect(partial(self.dataEntryButtonClicked, buttons['name'], entry_item))
            row_layout.addWidget(pb)
            row_layout.addWidget(entry_item)
            row_layout.addSpacing(20)

        row_layout.setAlignment(QtCore.Qt.AlignLeft)
        return(row_layout)

    def updateValues(self, struct):
        for n in struct['names']:
            r = self.entryItem.get(n)
            if r is not None:
                if isinstance(r, QtWidgets.QLineEdit):
                    self.entryItem[n].setText(struct[n]['value'])
                if isinstance(r, QtWidgets.QComboBox):
                    r.setCurrentIndex(1 + int(struct[n]['value']))

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

    def dataEntryButtonClicked(self, name, entryItem):

        if isinstance(entryItem, QtWidgets.QLineEdit):
            n = entryItem.text()
        if isinstance(entryItem, QtWidgets.QComboBox):
            n = entryItem.currentIndex() - 1
            if entryItem.currentIndex() == 0:
                self.statusText.setText("no change, dont select \"none\"")
                return()

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
    window = Mescaline()
    window.show()
    app.exec()
