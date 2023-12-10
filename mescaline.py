#!/usr/bin/env python3

import sys, re, math, json
import Payload, mescalineModuleLoad, FirstTab, StatusBar, appsTab, aboutTab
import importlib.util

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QGroupBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class Mescaline(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mescaline, self).__init__()

        ### Config file controls tab variables ### 
        file_path = "app_specs.json"
        try:
            with open(file_path, 'r') as json_file:
                try:
                    t = json.load(json_file)
                    self.tab_data = t['tab_data']
                    self.interface = t['interface']
                except json.JSONDecodeError as json_error:
                    print(f"Error decoding JSON: {json_error}")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")
            
        self.port_substring = self.interface["port_substring"]
        self.module_directory = self.interface["module_directory"]

        ### Window ### 
        self.setMinimumWidth(800)
        self.setMinimumHeight(300)

        ### Serial stuff ###
        self.port = QSerialPort()
        self.timer = QTimer(self) # timers are so helpful
        self.timer.timeout.connect(self.checkSerialStatus)
        self.timer.start(50)
        self.serialStreamingOn = False
        self.serialWasOn = False
        self.serialPayload = Payload.Payload()
        self.serialPayload.startTimer()

        ### Status Bar ###
        self.statusBar = StatusBar.createStatusBar(self)
        self.prevStatusText = ''

        ### First tab opens serial ###
        self.tabWidget = QtWidgets.QTabWidget()
        self.tab_first = FirstTab.FirstTab(self)
        self.tabWidget.addTab(self.tab_first,'Port')

        ### Next tabs are specified in input json ###
        self.tabs = self.makeTabs(self.tab_data)

        ### Get a list of apps available for spawning ###
        self.loadModules = mescalineModuleLoad.loadModules(self)
        self.classes_found = self.loadModules.testWithAST(self.module_directory)

        ### Tab to view the apps ###
        self.appsTab = appsTab.appsTab(self)
        self.tabWidget.addTab(self.appsTab,"Apps")

        ### Acknowledgements and user information ###
        self.aboutTab = aboutTab.aboutTab(self)
        self.tabWidget.addTab(self.aboutTab,"About")

        self.setWindowTitle("mescaline")
        self.setCentralWidget(self.tabWidget)

    def sendDataToApps(self, d):
        if len(self.loadModules.windowNames) > 0:
            for n in self.loadModules.windowNames:
                w = self.loadModules.windowPointers[n]
                if hasattr(w, 'receive_data'):
                    w.receive_data(d)

    ### Render tabs described in json config file ###
    def makeTabs(self, json_specs):
        tabs = []
        count = 0
        for t in json_specs.keys():
            self.tab_dict = json_specs[t]
            self.boxes = json_specs[t]['boxes']
            tab = createTab(self)
            tabs.append(tab)
            self.tabWidget.addTab(tab,json_specs[t]['title'])
        return(tabs)

    # closes all the spawned apps/windows
    def closeEvent(self, event):
        if len(self.loadModules.windowNames) > 0:
            for n in self.loadModules.windowNames:
                w = self.loadModules.windowPointers[n]
                if hasattr(w, 'close'):
                    w.close()
        event.accept()

    # things to do when a new serial-json string comes in
    def updateJsonData(self, str):
        str = str.rstrip('\n')
        d = {}
        for row in str.split('\n'):
            try:
                self.streamDict = json.loads(row)
                # there's different types of json that come down the pipe
                if self.streamDict.get('time'):
                    # print("LOG: {0}".format(self.streamDict))
                    pass
                if self.streamDict.get('vbus'):
                    # print("STATUS: {0}".format(self.streamDict))
                    self.updateStatusJson(self.streamDict) 
                self.sendDataToApps(self.streamDict)
            except json.JSONDecodeError as e:
                print("Getting bad json: {0}".format(row))


    # send the serial-json values to the status bar
    def updateStatusJson(self, streamDict):
        if streamDict.get('vbus'):
            f = round(streamDict['vbus'], 1)
            self.statusBar.vbusText.setText('Vbus:\n{0}'.format(f))

        if streamDict.get('iq') and streamDict.get('id'):
            f = math.sqrt((streamDict['iq'] * streamDict['iq']) + (streamDict['id'] * streamDict['id']))
            f = round(f, 1)
            self.statusBar.phaseAText.setText('PhaseA:\n{0}'.format(f))

        if streamDict.get('ehz'):
            self.statusBar.ehzText.setText('eHz:\n{0}'.format(round(streamDict['ehz'], 1)))
        if streamDict.get('TMOS'):
            self.statusBar.tmosText.setText('TMOS:\n{0}'.format(round(streamDict['TMOS'], 1)))
        if streamDict.get('TMOT'):
            self.statusBar.tmotText.setText('TMOT:\n{0}'.format(round(streamDict['TMOT'], 1)))

    # a lot of the tabs have values loaded from the mesc payload
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
    #  and changes colors of the buttons
    def checkSerialStatus(self):
        if self.port.isOpen(): 
            # Green hue = 0.33
            html_color = self.statusBar.buttonColorGenerator(frequency=.4, amplitude=0.5, phase_shift=0, hue = 0.33) 
            self.statusBar.getButton.setStyleSheet(f'background-color: {html_color}; border: 1px solid green;')
            self.statusBar.saveButton.setStyleSheet("background-color : #009900;" "border :1px solid green;") 
            self.serialWasOn = True
        else:
            self.statusBar.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            self.statusBar.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            if self.serialWasOn:
                self.statusBar.statusText.setText('Port died')

        # This gets reset when serial data has came in
        if (self.serialPayload.reportTimer()) > 0.2: 
            self.statusBar.serialButtonOff()
        else:
            self.statusBar.serialButtonOn()
                
### Creates a tab that is described in json config file
### 
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

    def updateValues(self, struct):
        for n in struct['names']:
            r = self.entryItem.get(n)
            if r is not None:
                if isinstance(r['entry_item'], QtWidgets.QLineEdit):
                    value = struct[n]['value']
                    if r.get('round'):
                        value = float(value)
                        rnd = int(r.get('round'))
                        value = round(value, rnd)
                        if rnd == 0:
                            value = int(value)
                        value = str(value)
                    r['entry_item'].setText(value)
                if isinstance(r['entry_item'], QtWidgets.QComboBox):
                    r['entry_item'].setCurrentIndex(1 + int(struct[n]['value']))

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
            self.entryItem[buttons['name']] = {}
            self.entryItem[buttons['name']]['entry_item'] = entry_item
            if buttons.get('round'):
                self.entryItem[buttons['name']]['round'] = buttons.get('round')
            entry_item.setFixedWidth(100)
            pb.setFixedWidth(120)
            pb.setToolTip(buttons['desc'])
            pb.clicked.connect(partial(self.dataEntryButtonClicked, buttons['name'], entry_item))
            row_layout.addWidget(pb)
            row_layout.addWidget(entry_item)
            row_layout.addSpacing(20)

        row_layout.setAlignment(QtCore.Qt.AlignLeft)
        return(row_layout)

    def isIntOrFloat(self, s):
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
            if self.isIntOrFloat(n):
                text = 'set {0} {1}'.format(name, n)
                self.statusText.setText(text)
                text = text + '\r\n'
                self.port.write( text.encode() )
            else:
                self.statusText.setText('{0} not number'.format(n))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mescaline()
    window.show()
    app.exec()

