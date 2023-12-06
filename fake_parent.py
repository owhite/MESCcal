#!/usr/bin/env python3

import sys
import sys, re, math, json
import Payload
import FirstTab, StatusBar
from functools import partial

import secondWindow

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTabWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QGroupBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class Mescaline(QtWidgets.QWidget):
    def __init__(self):
        super(Mescaline, self).__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.jsonList = []
        file_path = "fake.json"
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read and print each line
            for line in file:
                try:
                    self.jsonList.append(json.loads(line))
                    # self.send_data_to_new_window(self.streamDict)
                except json.JSONDecodeError as e:
                    print("Getting bad json: {0}".format(line))

        self.jsonListLen = len(self.jsonList)
        self.jsonListCounter = 0

        # Create a button
        self.vbusText = QtWidgets.QLabel('Vbus:\n  ')
        self.phaseAText = QtWidgets.QLabel('PhaseA:\n  ')
        self.tmosText = QtWidgets.QLabel('TMOS:\n  ')
        self.tmotText = QtWidgets.QLabel('TMOT:\n  ')
        self.ehzText = QtWidgets.QLabel('eHz:\n  ')

        self.runDataButton = QtWidgets.QPushButton('Run')
        self.runDataButton.clicked.connect(self.run_json_data)
        self.runDataButton.setCheckable(True)
        self.runDataButton.setStyleSheet("background-color: white; border: 1px solid green;")

        self.winOpenButton = QtWidgets.QPushButton('Win')
        self.winOpenButton.clicked.connect(self.open_new_window)
        self.winOpenButton.setCheckable(True)
        self.winOpenButton.setStyleSheet("background-color: white; border: 1px solid green;")

        layout.addWidget(self.runDataButton)
        layout.addWidget(self.vbusText)
        layout.addWidget(self.phaseAText)
        layout.addWidget(self.tmosText)
        layout.addWidget(self.tmotText)
        layout.addWidget(self.ehzText)
        layout.addWidget(self.winOpenButton)

        self.streamTimer = QTimer(self)
        self.streamTimer.timeout.connect(self.send_data_to_new_window)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('File Dialog Example')
        self.show()

    def send_data_to_new_window(self):
        print(self.jsonListCounter)
        self.jsonListCounter += 1
        if self.jsonListCounter > self.jsonListLen:
            self.jsonListCounter = 0

        d = self.jsonList[self.jsonListCounter]
        self.updateStatusJson(d)
        if hasattr(self, 'new_window'):
            self.new_window.receive_data(d)

    def updateStatusJson(self, streamDict):
        f = round(streamDict['vbus'], 1)
        self.vbusText.setText('Vbus:\n{0}'.format(f))

        f = math.sqrt((streamDict['iq'] * streamDict['iq']) + (streamDict['id'] * streamDict['id']))
        f = round(f, 1)
        self.phaseAText.setText('PhaseA:\n{0}'.format(f))

        self.ehzText.setText('eHz:\n{0}'.format(round(streamDict['ehz'], 1)))
        self.tmosText.setText('TMOS:\n{0}'.format(round(streamDict['TMOS'], 1)))
        self.tmotText.setText('TMOT:\n{0}'.format(round(streamDict['TMOT'], 1)))

    def run_json_data(self):
         if self.runDataButton.isChecked():
            self.runDataButton.setStyleSheet("background-color: lightgreen; border: 1px solid green;")
            self.streamTimer.start(100)
         else:
             self.runDataButton.setStyleSheet("background-color: white; border: 1px solid green;")
             self.streamTimer.stop()

    def open_new_window(self, flag):
        if self.winOpenButton.isChecked():
            self.winOpenButton.setStyleSheet("background-color: lightgreen; border: 1px solid green;")
            self.new_window = secondWindow.secondWindow()
            self.new_window.show()
        else:
            self.winOpenButton.setStyleSheet("background-color: white; border: 1px solid green;")
            # self.winOpenButton.setChecked(False)
            if hasattr(self, 'new_window'):
                self.new_window.close()

    def close_new_window(self):
        if hasattr(self, 'new_window'):
            print("closing window")
            self.new_window.close()


    def closeEvent(self, event):
        # Override the closeEvent method to detect when the window is closed
        print("Main window closing")
        if hasattr(self, 'new_window'):
            print("closing window")
            self.new_window.close()
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mescaline()
    window.show()
    app.exec()

