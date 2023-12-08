#!/usr/bin/env python3

import sys
import sys, re, math, json
import Payload, mescalineModuleLoad
import FirstTab, StatusBar, appsTab
import importlib.util

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

        self.loadModules = mescalineModuleLoad.loadModules()

        self.module_directory = './APPS'

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
        self.statusBar = StatusBar.createStatusBar(self)
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

        # Specify the directory containing the modules
        self.classes_found = self.loadModules.testWithAST(self.module_directory)
        print(f'Classes found in {self.module_directory}: {self.classes_found}')
        self.windows = self.loadModules.load(self.module_directory, self.classes_found)

        self.appsWidget = QtWidgets.QTabWidget()
        self.appsTab = appsTab.appsTab(self)
        self.tabWidget.addTab(self.appsTab,"APPs")

        # self.tabWidget.setCurrentIndex(p)

        self.setWindowTitle("Mescaline")

        self.setCentralWidget(self.tabWidget)

    def open_new_window(self, flag):
        if self.statusBar.winOpenButton.isChecked():
            self.statusBar.winOpenButton.setStyleSheet("background-color: lightgreen; border: 1px solid green;")
            # self.new_window = secondWindow.secondWindow()
            self.new_window = drawThermo.Thermometer()
            self.new_window.show()
        else:
            self.statusBar.winOpenButton.setStyleSheet("background-color: white; border: 1px solid green;")
            # self.statusBar.winOpenButton.setChecked(False)
            if hasattr(self, 'new_window'):
                self.new_window.close()

    def send_data_to_new_window(self, d):
        if len(self.windows) > 0:
            for w in self.windows:
                if hasattr(w, 'receive_data'):
                    w.receive_data(d)

    def closeEvent(self, event):
        # Override the closeEvent method to detect when the window is closed
        print("Main window closing")
        if len(self.windows) > 0:
            for w in self.windows:
                if hasattr(w, 'receive_data'):
                    w.close()
        event.accept()

    def updateJsonData(self, str):
        str = str.rstrip('\n')
        d = {}
        for row in str.split('\n'):
            try:
                self.streamDict = json.loads(row)
                self.updateStatusJson(self.streamDict)
                self.send_data_to_new_window(self.streamDict)
            except json.JSONDecodeError as e:
                print("Getting bad json: {0}".format(row))


    def updateStatusJson(self, streamDict):
        f = round(streamDict['vbus'], 1)
        self.statusBar.vbusText.setText('Vbus:\n{0}'.format(f))

        f = math.sqrt((streamDict['iq'] * streamDict['iq']) + (streamDict['id'] * streamDict['id']))
        f = round(f, 1)
        self.statusBar.phaseAText.setText('PhaseA:\n{0}'.format(f))

        self.statusBar.ehzText.setText('eHz:\n{0}'.format(round(streamDict['ehz'], 1)))
        self.statusBar.tmosText.setText('TMOS:\n{0}'.format(round(streamDict['TMOS'], 1)))
        self.statusBar.tmotText.setText('TMOT:\n{0}'.format(round(streamDict['TMOT'], 1)))

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

    # a timer that checks if anything has recently been transmitted
    def checkSerialStatus(self):
        if not self.port.isDataTerminalReady(): # seems to indicate the port is dead
            self.statusBar.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            self.statusBar.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            if self.serialWasOn:
                self.statusBar.statusText.setText('Port died')
        else:
            html_color = self.statusBar.buttonColorGenerator(frequency=.4, amplitude=0.5, phase_shift=0, hue = 0.33) # Green hue = 0.33
            self.statusBar.getButton.setStyleSheet(f'background-color: {html_color}; border: 1px solid green;')
            self.statusBar.saveButton.setStyleSheet("background-color : #009900;" "border :1px solid green;") 
            self.serialWasOn = True

        if (self.serialPayload.reportTimer()) > 0.2: # checks if json is coming in
            self.statusBar.serialButtonOff()
        else:
            self.statusBar.serialButtonOn()
                
class createTab(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.tab_dict = parent.tab_dict
        self.boxes = self.tab_dict['boxes']
        self.tab_title = self.tab_dict['title']
        self.port = parent.port
        self.statusText = parent.statusBar.statusText
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

