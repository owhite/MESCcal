import re
import time
import math
import colorsys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QTabWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtGui import QPainter, QPainterPath

class createStatusBar(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStatusBar = parent.setStatusBar
        self.statusBar = parent.statusBar
        self.port = parent.port
        self.serialPayload = parent.serialPayload
        self.initUI()

    def initUI(self):
        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar( self.status_bar )

        # Create a widget to hold the layout
        self.layout_widget = QtWidgets.QWidget(self)

        # Create a vertical layout for the widget
        layout = QtWidgets.QVBoxLayout(self.layout_widget)

        container1 = QtWidgets.QWidget()
        h1 = QtWidgets.QHBoxLayout(container1)

        # Create buttons
        self.getButton = CapsuleButton("Get")
        self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid black;") 
        self.getButton.clicked.connect(self.getSerialData)
        self.getButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Get: retreive values from MESC, load into tabs")
        self.getButton.leaveEvent = self.customButtonHoverLeave
        QTimer.singleShot(100, lambda: self.getButton.enterEvent(None)) # does a little refresh that helps

        self.saveButton = CapsuleButton("Set")
        self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid black;") 
        self.saveButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Save: store all values in MESC")
        self.saveButton.leaveEvent = self.customButtonHoverLeave
        self.saveButton.clicked.connect(self.saveSerialData)

        self.streamButton = CapsuleButton("Data")
        self.streamButton.setStyleSheet("background-color : white;" "border :1px solid black;") 
        self.streamButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Data: toggles data streaming from MESC")
        self.streamButton.leaveEvent = self.customButtonHoverLeave
        self.streamButton.setCheckable(True)
        self.streamButton.clicked.connect(self.getSerialStream)

        self.statusText = QtWidgets.QLabel(self)
        self.statusText.setText('Status msgs here')
        self.statusText.setAlignment(QtCore.Qt.AlignRight)

        h1.addWidget(self.getButton)
        h1.addWidget(self.saveButton)
        h1.addWidget(self.streamButton)

        self.vbusText = QtWidgets.QLabel('Vbus:\n  ')
        self.phaseAText = QtWidgets.QLabel('PhaseA:\n  ')
        self.tmosText = QtWidgets.QLabel('TMOS:\n  ')
        self.tmotText = QtWidgets.QLabel('TMOT:\n  ')
        self.ehzText = QtWidgets.QLabel('eHz:\n  ')

        # self.winOpenButton = QtWidgets.QPushButton('Win')
        # self.winOpenButton.clicked.connect(self.open_new_window)
        # self.winOpenButton.setCheckable(True)
        # self.winOpenButton.setStyleSheet("background-color: white; border: 1px solid green;")

        h1.addWidget(self.vbusText)
        h1.addWidget(self.phaseAText)
        h1.addWidget(self.tmosText)
        h1.addWidget(self.tmotText)
        h1.addWidget(self.ehzText)
        # h1.addWidget(self.winOpenButton)
        layout.addWidget(container1)

        self.status_bar.addWidget(self.layout_widget)
        self.statusBar().addPermanentWidget( self.statusText )

    def customButtonHoverEnter(self, event, message):
        self.prevStatusText = self.statusText.text()
        self.statusText.setText(message)

    def customButtonHoverLeave(self, event):
        # I didnt like how this behaves, just clear the text
        # self.statusText.setText(self.prevStatusText)
        self.statusText.setText('Status msgs here')

    def serialButtonOff(self):
        self.streamButton.setStyleSheet("background-color : white;" "border :2px solid black;") 
        self.streamButton.setChecked(True)
        self.serialStreamingOn = False

    def serialButtonOn(self):
        # Green hue = 0.33 -- not sure how it works
        html_color = self.buttonColorGenerator(frequency=.4, amplitude=0.8, phase_shift=0, hue = 0.77) 
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
        lightness = (1 - value) - .2
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        html_color = "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))
        return html_color

class CapsuleButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super(CapsuleButton, self).__init__(text, parent)
        self.setFixedHeight(24)
        self.setFixedWidth(32)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, rect.height() / 2, rect.height() / 2)
        painter.fillPath(path, self.palette().button())
        painter.setPen(Qt.black)
        painter.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)
        painter.setPen(self.palette().text().color())
        painter.drawText(rect, Qt.AlignCenter, self.text())
