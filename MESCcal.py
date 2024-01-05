#!/usr/bin/env python3

import qdarkgraystyle

import sys, re, math, json, platform
import Payload, MESCcalModuleLoad, FirstTab, StatusBar, appsTab
import aboutTab, howtoTab, presetsTab, ColorSegmentRing
from NumericalInputPad import NumericalInputPad
import Events
import importlib.util

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout
from PyQt5.QtWidgets import QGroupBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class MESCcal(QtWidgets.QMainWindow):
    def __init__(self):
        super(MESCcal, self).__init__()

        ### Config file controls tab variables ### 
        file_path = "app_specs.json"
        try:
            with open(file_path, 'r') as json_file:
                try:
                    t = json.load(json_file)
                    self.tab_data = t['tab_data']
                    self.interface = t['interface']
                    self.presets = t['presets']
                except json.JSONDecodeError as json_error:
                    print(f"Error decoding JSON: {json_error}")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")
            
        ### global set of QLineEdit() boxes that will may get input from virtual keyboard
        self.lineEditBoxes = []

        self.port_substring = self.interface["port_substring"]
        self.module_directory = self.interface["module_directory"]

        system = platform.system()

        self.os = 'Mac'
        if system == "Windows":
            self.os = 'Win'
            self.min_width = 1200
            self.min_height = 800
        else:
            self.os = 'Mac'
            self.min_width = 480
            self.min_height = 300

        self.numerical_pad_status = False

        ### Window ### 
        self.setMinimumWidth(self.min_width)
        self.setMinimumHeight(self.min_height)

        ### Serial stuff ###
        self.port = QSerialPort()
        self.timer = QTimer(self) # timers are so helpful
        self.timer.timeout.connect(self.checkSerialStatus)
        self.timer.start(50)
        self.serialStreamingOn = False
        self.serialWasOn = False
        self.serialPayload = Payload.Payload()
        self.serialPayload.startTimer()
        self.serialStreamingOn = False

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
        self.module_directory = './APPS'
        self.loadModules = MESCcalModuleLoad.loadModules(self)
        self.modules_dict = self.loadModules.testWithAST(self.module_directory)
        self.classes_found = self.modules_dict['dict']

        ### Tab to view the apps ###
        self.appsTab = appsTab.appsTab(self)
        self.tabWidget.addTab(self.appsTab,"Apps")

        ### Presets to make user happy
        self.presetsTab = presetsTab.presetsTab(self)
        self.tabWidget.addTab(self.presetsTab,"Presets")
        self.tabs.append(self.presetsTab) # this guy gets updates so add to list

        ### Acknowledgements and user information ###
        self.howtoTab = howtoTab.howtoTab(self)
        self.tabWidget.addTab(self.howtoTab,"How to")

        system = platform.system()

        ### Acknowledgements and user information ###
        self.aboutTab = aboutTab.aboutTab(self)
        self.tabWidget.addTab(self.aboutTab,"About")

        self.setWindowTitle("MESCcal ({0})".format(self.os))
        self.setCentralWidget(self.tabWidget)

        self.tabWidget.currentChanged.connect(self.tab_changed)

    def keyPressEvent(self, event):
        print("MAIN")
        if event.text() == 'g':
            print("get")
        if event.text() == 'o':
            print("open")
        if event.text() == 'd':
            print("switch forward")
            current_tab_index = self.tabWidget.currentIndex()
            next_tab_index = (current_tab_index + 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(next_tab_index)
        if event.text() == 'a':
            print("switch back")
            current_tab_index = self.tabWidget.currentIndex()
            next_tab_index = (current_tab_index - 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(next_tab_index)
        

    def virtualButtonClicked(self, value):
        print("VIRTUAL {0}".format(value))

        for b in self.lineEditBoxes:
            if b.hasFocus():
                b.setText(b.text() + value)
                print("focus {0}".format(b.text()))

    def toggle_status_bar(self, checked):
        self.statusBar.toggle_status_bar(checked)

    def sendDataToApps(self, d):
        if len(self.loadModules.windowNames) > 0:
            for n in self.loadModules.windowNames:
                w = self.loadModules.windowPointers[n]
                if hasattr(w, 'receive_data'):
                    w.receive_data(d)
                if hasattr(w, 'set_port'):
                    w.set_port(self.port)

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

    # things to do when a new serial-json string comes in.
    #  this feeds the results from json to the status bar
    #  and the apps
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
                    self.statusBar.updateStatusJson(self.streamDict)
                self.sendDataToApps(self.streamDict)
            except json.JSONDecodeError as e:
                print("Getting bad json: {0}".format(row))

    # things to do when NON json data comes in
    #  theres a lot of tabs that show data, update those tabs
    #  this is selective, some strings that come in are
    #  ignored for now
    def updateTabs(self):
        if len(self.serialPayload.reportString()) > 0:
            self.serialPayload.parsePayload()
            p = self.serialPayload.reportPayload()
            # print("names: {0}".format(p['names']))
            # update tabs if the payload has anything, 
            if p is not None and len(p['names']) > 0:
                for tab in self.tabs:
                    tab.updateValues(p)

            self.statusBar.updateStatusPayload(p)

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
            self.statusBar.getButton.setStyleSheet("background-color :  #F39C12;" "border :1px solid green;") 
            self.statusBar.saveButton.setStyleSheet("background-color :  #F39C12;" "border :1px solid green;") 
            if self.serialWasOn:
                self.statusBar.statusText.setText('Port died')

        # This gets reset when serial data has came in
        if (self.serialPayload.reportTimer()) > 0.2: 
            self.statusBar.serialButtonOff()
        else:
            self.statusBar.serialButtonOn()
                
    def dataEntryButtonClicked(self, name, entryItem):
        print("DATA ENTRY CLICKED")
        if isinstance(entryItem, QtWidgets.QLineEdit):
            n = entryItem.text()
        if isinstance(entryItem, QtWidgets.QComboBox):
            n = entryItem.currentIndex() - 1
            if entryItem.currentIndex() == 0:
                self.statusBar.statusText.setText("no change, dont select \"none\"")
                return()

        if self.numerical_pad_status:
            numerical_input_pad = NumericalInputPad(self, name, n)
            numerical_input_pad.show()  
        else:
            if not self.port.isOpen():
                self.statusBar.statusText.setText('Port closed: cant update')
            else:
                if self.isIntOrFloat(n):
                    text = 'set {0} {1}'.format(name, n)
                    self.statusBar.statusText.setText(text)
                    text = text + '\r\n'
                    self.port.write( text.encode() )
                else:
                    self.statusBar.statusText.setText('{0} not number'.format(n))

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

    def tab_changed(self, index):
        current_tab_name = self.tabWidget.tabText(index)
        if current_tab_name == 'Presets':
            self.presetsTab.updateThisTab()
        if current_tab_name == 'About':
            self.aboutTab.updateThisTab()


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
        self.dataEntryButtonClicked = parent.dataEntryButtonClicked
        self.tabWidget = parent.tabWidget
        self.initUI()

    def initUI(self):
        self.buttons =[]
        self.entryItem ={}

        self.widget_list = []

        self.setCentralWidget( QtWidgets.QWidget(self) )
        tab_layout = QtWidgets.QFormLayout( self.centralWidget() )

        for box in self.boxes:
            button_rows = box['buttons']
            tab_layout.addWidget(self.createBox(box['name'], button_rows))

    # totally do not understand why some keyPressEvents go to this tab versus the
    #   main program -- but dont really care. 
    def keyPressEvent(self, event):
        if event.text() == 'g':
            print("get")
        elif event.text() == 'd':
            print("switch forward")
            current_tab_index = self.tabWidget.currentIndex()
            next_tab_index = (current_tab_index + 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(next_tab_index)
        elif event.text() == 'a':
            print("switch back")
            current_tab_index = self.tabWidget.currentIndex()
            next_tab_index = (current_tab_index - 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(next_tab_index)

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

    def eventFilter(self, obj, event):
        if isinstance(obj, QtWidgets.QLineEdit):
            if event.type() == QtCore.QEvent.FocusIn:
                obj.setStyleSheet("background-color: grey;")
                print(f"E1 Focus In: {obj.objectName()}")
            elif event.type() == QtCore.QEvent.FocusOut:
                obj.setStyleSheet("")
                print(f"E1 Focus Out: {obj.objectName()}")
            elif event.type() == event.KeyPress:
                key = event.key()
                print(f'Key Pressed: {key}')
                if event.key() == Qt.Key_Left:
                    self.setFocusToPreviousWidget(obj)
                elif event.key() == Qt.Key_Right:
                    self.setFocusToNextWidget(obj)
                elif event.key() == Qt.Key_Return:
                    print("return pressed")

        if isinstance(obj, QtWidgets.QComboBox):
            if event.type() == QtCore.QEvent.FocusIn:
                obj.setStyleSheet("background-color: grey;")
                print(f"E2 Focus2 In: {obj.objectName()}")
            elif event.type() == QtCore.QEvent.FocusOut:
                obj.setStyleSheet("")
                print(f"E2 Focus2 Out: {obj.objectName()}")
            elif event.type() == event.KeyPress:
                key = event.key()
                print(f'Key Pressed2: {key}')
                if event.key() == Qt.Key_Left:
                    self.setFocusToPreviousWidget(obj)
                elif event.key() == Qt.Key_Right:
                    self.setFocusToNextWidget(obj)
                elif event.key() == Qt.Key_Return:
                    print("return pressed")

        return super().eventFilter(obj, event)

    def setFocusToPreviousWidget(self, current_widget):
        if current_widget:
            index = self.widget_list.index(current_widget)
            prev_index = (index - 1) % len(self.widget_list)
            self.widget_list[prev_index].setFocus()

    def setFocusToNextWidget(self, current_widget):
        if current_widget:
            index = self.widget_list.index(current_widget)
            next_index = (index + 1) % len(self.widget_list)
            self.widget_list[next_index].setFocus()

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
                entry_item.installEventFilter(self)
                entry_itemEvent = Events.HLComboBox(entry_item, self.widget_list)

            else:
                entry_item = QtWidgets.QLineEdit()
                entry_item.installEventFilter(self)
                entry_itemEvent = Events.HLLineEdit(entry_item, self.widget_list)
                
            self.entryItem[buttons['name']] = {}
            self.entryItem[buttons['name']]['entry_item'] = entry_item
            if buttons.get('round'):
                self.entryItem[buttons['name']]['round'] = buttons.get('round')
            entry_item.setFixedWidth(100)

            pb = QtWidgets.QPushButton(buttons['name'])
            pbEvent = Events.HLButton(pb)
            pb.setFixedWidth(120)
            pb.setToolTip(buttons['desc'])
            pb.clicked.connect(partial(self.dataEntryButtonClicked, buttons['name'], entry_item))

            row_layout.addWidget(pb)
            row_layout.addWidget(entry_item)
            self.widget_list.append(pb)
            self.widget_list.append(entry_item)

            row_layout.addSpacing(20)

        row_layout.setAlignment(QtCore.Qt.AlignLeft)
        return(row_layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    window = MESCcal()
    window.show()
    app.exec()

