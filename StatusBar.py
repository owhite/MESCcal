import re
import time
import math
import colorsys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class createStatusBar(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStatusBar = self.parent.setStatusBar
        self.statusBar = self.parent.statusBar
        self.port = self.parent.port
        self.initUI()

    def initUI(self):
        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar( self.status_bar )
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
        self.status_bar.addWidget(self.layout_widget)

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
        # Green hue = 0.33 -- not sure how it works
        html_color = self.buttonColorGenerator(frequency=.4, amplitude=0.5, phase_shift=0, hue = 0.77) 
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


        
