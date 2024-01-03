import re
import time
import math
import colorsys
import ColorSegmentRing
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QTabWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtGui import QPainter, QPainterPath

### Tab that handles displaying status of the serial,
###    screens to show output of serial
###    status information like vbus, and
###    has some buttons to perform things.
###    This gets called by main program.
### 
class createStatusBar(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStatusBar = parent.setStatusBar
        self.serialStreamingOn = False
        self.statusBar = parent.statusBar
        self.port = parent.port
        self.os = parent.os
        self.serialPayload = parent.serialPayload
        # self.height() = parent.height()

        self.initUI()

    def initUI(self):
        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar( self.status_bar )

        # Create a widget to hold the layout
        self.layout_widget = QtWidgets.QWidget(self)

        # Create a vertical layout for the widget
        self.layout = QtWidgets.QVBoxLayout(self.layout_widget)

        self.container1 = QtWidgets.QWidget()
        h1 = QtWidgets.QHBoxLayout(self.container1)

        # Create buttons
        self.getButton = CapsuleButton(self, "Get")
        self.getButton.setStyleSheet("background-color :  #F39C12;" "border :1px solid black;") 
        self.getButton.clicked.connect(self.getSerialData)
        self.getButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Get: retreive values from MESC for tabs")
        self.getButton.leaveEvent = self.customButtonHoverLeave
        QTimer.singleShot(100, lambda: self.getButton.enterEvent(None)) # does a little refresh that helps

        self.saveButton = CapsuleButton(self, "Set")
        self.saveButton.setStyleSheet("background-color :  #F39C12;" "border :1px solid black;") 
        self.saveButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Save: store all values in MESC")
        self.saveButton.leaveEvent = self.customButtonHoverLeave
        self.saveButton.clicked.connect(self.saveSerialData)

        self.streamButton = CapsuleButton(self, "Data")
        self.streamButton.setStyleSheet("background-color : #F39C12;" "border :1px solid black;") 
        self.streamButton.clicked.connect(self.getSerialStream)
        self.streamButton.enterEvent = lambda event: self.customButtonHoverEnter(event, "Data: toggles data streaming from MESC")
        self.streamButton.leaveEvent = self.customButtonHoverLeave
        self.streamButton.setCheckable(True)

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
        self.errorText = QtWidgets.QLabel('Error:\n  ')

        self.adc1_ring = ColorSegmentRing.colorSegmentRing()
        self.adc1_ring.setVisible(True)
        self.adc1_ring.ring_text = 'adc1'
        self.adc1_ring.ring_text_size = 12
        if self.os == 'Win':
            self.adc1_ring.ring_text_size = 6

        h1.addWidget(self.vbusText)
        h1.addWidget(self.phaseAText)
        h1.addWidget(self.tmosText)
        h1.addWidget(self.tmotText)
        h1.addWidget(self.ehzText)
        h1.addWidget(self.errorText)
        h1.addWidget(self.adc1_ring)

        # h1.addWidget(self.winOpenButton)
        self.layout.addWidget(self.container1)

        self.status_bar.addWidget(self.layout_widget)
        self.statusBar().addPermanentWidget( self.statusText )

    # manage data coming from get
    def updateStatusPayload(self, struct):
        adc1_min = None
        adc1_max = None
        for n in struct['names']:
            if n == 'adc1_min':
                adc1_min = struct[n].get('value')
            if n == 'adc1_max':
                adc1_max = struct[n].get('value')
        if adc1_min is not None and adc1_max is not None:
            self.adc1_ring.setMinMax(int(adc1_min), int(adc1_max))
            self.adc1_ring.repaint()

    # manage the incoming serial-json values 
    def updateStatusJson(self, streamDict):
        if streamDict.get('vbus') is not None:
            f = round(streamDict['vbus'], 1)
            self.vbusText.setText('Vbus:\n{0}'.format(f))

        if streamDict.get('iq') and streamDict.get('id'):
            f = math.sqrt((streamDict['iq'] * streamDict['iq']) + (streamDict['id'] * streamDict['id']))
            f = round(f, 1)
            self.phaseAText.setText('PhaseA:\n{0}'.format(f))

        if streamDict.get('ehz') is not None:
            self.ehzText.setText('eHz:\n{0}'.format(round(streamDict['ehz'], 1)))
        if streamDict.get('TMOS') is not None:
            self.tmosText.setText('TMOS:\n{0}'.format(round(streamDict['TMOS'], 1)))
        if streamDict.get('TMOT') is not None:
            self.tmotText.setText('TMOT:\n{0}'.format(round(streamDict['TMOT'], 1)))
        if streamDict.get('error') is not None:
            self.errorText.setText('error:\n{0}'.format(streamDict['error']))
        if streamDict.get('adc1') is not None:
            self.adc1_ring.value = streamDict['adc1']
            self.adc1_ring.repaint()

    def customButtonHoverEnter(self, event, message):
        self.prevStatusText = self.statusText.text()
        self.statusText.setText(message)

    def customButtonHoverLeave(self, event):
        # I didnt like how this behaves, just clear the text
        # self.statusText.setText(self.prevStatusText)
        self.statusText.setText('Status msgs here')

    def serialButtonOff(self):
        self.streamButton.setStyleSheet("background-color : #F39C12;" "border :2px solid black;") 
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
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.text = text
        self.os = parent.os
        self.setFixedHeight(24)
        self.setFixedWidth(32)
        if self.os == 'Win':
            self.setFixedHeight(32)
            self.setFixedWidth(50)

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
        painter.drawText(rect, Qt.AlignCenter, self.text)
