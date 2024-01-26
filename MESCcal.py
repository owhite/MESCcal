#!/usr/bin/env python3

import sys, re, math, json, platform
from configparser import ConfigParser
import Payload, MESCcalModuleLoad, FirstTab, StatusBar, appsTab, createTab, speedoTab
import aboutTab, howtoTab, presetsTab, ColorSegmentRing
from NumericalInputPad import NumericalInputPad
import importlib.util

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout
from PyQt5.QtWidgets import QGroupBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

import qdarkgraystyle
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # stop annoying messages
import pygame

class MESCcal(QtWidgets.QMainWindow):
    def __init__(self):
        super(MESCcal, self).__init__()

        self.installEventFilter(self)

        ### Config file controls tab variables ### 
        file_path = "app_specs.json"
        try:
            with open(file_path, 'r') as json_file:
                try:
                    t = json.load(json_file)
                    self.tab_data = t['tab_data']
                    self.presets = t['presets']
                except json.JSONDecodeError as json_error:
                    print(f"Error decoding JSON: {json_error}")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")
            
        ### Config file controls UI variables ### 
        config = ConfigParser()
        try:
            with open('app_specs.ini', 'r') as configfile:
                config.read_file(configfile)
        except FileNotFoundError:
            print("Config file not found")

        self.keyPressSound = [False]  # Use a list to hold a mutable object
        self.useKeypresses = [False]

        if config.get('Settings', 'use_keypresses') == 'True':
            self.useKeypresses = [True]
        if config.get('Settings', 'use_keypress_sound') == 'True':
            self.keyPressSound = [True]

        self.port_substring = config.get('Settings', 'port_substring')
        self.module_directory = config.get('Settings', 'module_directory')

        system = platform.system()

        self.os = 'Mac'
        if system == "Windows":
            self.os = 'Win'
            self.min_width = 1200
            self.min_height = 800
        else:
            self.os = 'Mac'
            self.min_width = 600
            self.min_height = 480

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

        pygame.mixer.init(channels=1, buffer=1024)
        pygame.mixer.music.load('./soundfile.wav')

        ### Status Bar ###
        self.statusBar = StatusBar.createStatusBar(self)
        self.prevStatusText = ''

        self.updateTabs = []

        ### Speedo ### 
        self.tabWidget = QtWidgets.QTabWidget()
        self.speedoTab = speedoTab.SpeedoTab(self)
        self.tabWidget.addTab(self.speedoTab, "speedo")
        self.updateTabs.append(self.speedoTab)
        
        ### First tab opens serial ###
        self.tab_first = FirstTab.FirstTab(self)
        self.tabWidget.addTab(self.tab_first,'Port')
        self.updateTabs.append(self.tab_first)

        ### Next tabs are specified in input json ###
        self.makeTabs(self.tab_data)

        ### Get a list of apps available for spawning ###
        self.module_directory = './APPS'
        self.loadModules = MESCcalModuleLoad.loadModules(self)
        self.modules_dict = self.loadModules.testWithAST(self.module_directory)
        self.classes_found = self.modules_dict['dict']

        ### Tab to view the apps ###
        self.appsTab = appsTab.appsTab(self)
        self.tabWidget.addTab(self.appsTab,"Apps")
        self.updateTabs.append(self.appsTab)

        ### Presets to make user happy
        self.presetsTab = presetsTab.presetsTab(self)
        self.tabWidget.addTab(self.presetsTab,"Presets")
        self.updateTabs.append(self.presetsTab)

        ### Acknowledgements and user information ###
        self.howtoTab = howtoTab.howtoTab(self)
        self.tabWidget.addTab(self.howtoTab,"How to")
        self.updateTabs.append(self.howtoTab)

        system = platform.system()

        ### Acknowledgements and user information ###
        self.aboutTab = aboutTab.aboutTab(self)
        self.tabWidget.addTab(self.aboutTab,"About")
        self.updateTabs.append(self.aboutTab)

        self.setWindowTitle("MESCcal ({0})".format(self.os))
        self.setCentralWidget(self.tabWidget)

        self.tabWidget.currentChanged.connect(self.tab_changed)

    def key_sound(self):
        if self.keyPressSound[0]:
            pygame.mixer.music.play()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Right:
                print("Right key pressed in central widget.")
                # Do something with the key event if needed
                return True  # Event handled
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_G:
            self.key_sound()
            print("MAIN: get")
        elif key == Qt.Key_O:
            self.key_sound()
            print("MAIN: open")
        elif key == Qt.Key_D:
            print("MAIN: switch forward")
            self.key_sound()
            current_tab_index = self.tabWidget.currentIndex()
            next_tab_index = (current_tab_index + 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(next_tab_index)
        elif key == Qt.Key_A:
            print("MAIN: switch back")
            self.key_sound()
            current_tab_index = self.tabWidget.currentIndex()
            next_tab_index = (current_tab_index - 1) % self.tabWidget.count()
            self.tabWidget.setCurrentIndex(next_tab_index)
        else:
            super().keyPressEvent(event)

    def toggle_status_bar(self, checked):
        self.statusBar.toggle_status_bar(checked)

    # for the toys that are in the apps directory
    def sendDataToApps(self, d):
        if len(self.loadModules.windowNames) > 0:
            for n in self.loadModules.windowNames:
                w = self.loadModules.windowPointers[n]
                if hasattr(w, 'receive_data'):
                    w.receive_data(d)
                if hasattr(w, 'set_port'):
                    w.set_port(self.port)

    # for any of the tabs that might be displaying live data
    def sendDataToTabs(self, d):
        for tab in self.updateTabs:
            if hasattr(tab, 'updateValuesWithStream'):
                tab.updateValuesWithStream(d)


    ### Render tabs described in json config file ###
    def makeTabs(self, json_specs):
        count = 0
        for t in json_specs.keys():
            self.tab_dict = json_specs[t]
            self.boxes = json_specs[t]['boxes']
            tab = createTab.createTab(self)
            self.updateTabs.append(tab)
            self.tabWidget.addTab(tab,json_specs[t]['title'])

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
                self.sendDataToTabs(self.streamDict)
            except json.JSONDecodeError as e:
                print("Getting bad json: {0}".format(row))

    # things to do when NON json data comes in
    #  theres a lot of tabs that show data, update those tabs
    #  this is selective, some strings that come in are
    #  ignored for now
    def updateTabsWithGet(self):
        if len(self.serialPayload.reportString()) > 0:
            self.serialPayload.parsePayload()
            p = self.serialPayload.reportPayload()
            # print("names: {0}".format(p['names']))
            # update tabs if the payload has anything, 
            if p is not None and len(p['names']) > 0:
                for tab in self.updateTabs:
                    if hasattr(tab, 'updateValuesWithGet'):
                        tab.updateValuesWithGet(p)

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
        # if current_tab_name == 'About':
            # self.aboutTab.updateThisTab()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    window = MESCcal()
    window.show()
    app.exec()

