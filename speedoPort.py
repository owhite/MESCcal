import re
import time
import math
import colorsys
import ColorSegmentRing
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QSpacerItem
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtGui import QKeyEvent, QPalette, QColor, QPainter, QPainterPath

### Port connection tab -- handles serial connection and sending commands
###
class Port(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.serialPayload = parent.serialPayload
        self.port_substring = parent.port_substring
        self.max_chars = 3000
        self.sound = parent.sound
        self.keyPressSound = parent.keyPressSound

        self.initUI()

    def initUI(self):
        ### Serial stuff ###
        self.port = QSerialPort()
        self.timer = QTimer(self) # timers are so helpful
        self.timer.timeout.connect(self.checkSerialStatus)
        self.timer.start(50)
        self.serialStreamingOn = False
        self.serialWasOn = False

        self.statusText = QtWidgets.QLabel(self)

        self.buttonColor = '#2E4053' 

        self.jsonData = QtWidgets.QTextEdit(self) # making this one in the parent
        self.jsonDataView   = jsonDataView(self)
        self.serialDataView = SerialDataView(self) # these make their own QTextEdit boxes

        self.serialSendView = SerialSendView(self)
        self.serialSendView.serialSendSignal.connect(self.sendFromPort)

        self.port.readyRead.connect(self.readFromPort)

        self.setCentralWidget( QtWidgets.QWidget(self) )
        layout = QtWidgets.QVBoxLayout( self.centralWidget() )

        self.widgets = {}
        self.widget_index = 0

        ### Tool Bar -- top banner on the port tab ###
        self.toolBar = ToolBar(self)
        self.addToolBar(self.toolBar)
        self.portGetButton = self.toolBar.portGetButton
        self.portOpenButton = self.toolBar.portOpenButton
        self.portStreamButton = self.toolBar.portStreamButton
        
        layout.addWidget(self.jsonDataView)
        layout.addWidget(self.serialDataView)
        layout.addWidget(self.serialSendView)
        layout.setContentsMargins(3, 3, 3, 3)

        self.widget_index = 0

    # a timer that checks if anything has recently been transmitted
    #  and changes colors of the buttons
    def checkSerialStatus(self):
        if self.port.isOpen(): 
            # Green hue = 0.33
            html_color = self.buttonColorGenerator(frequency=.4, amplitude=0.5, phase_shift=0, hue = 0.33) 
            self.portOpenButton.setStyleSheet(f'background-color: {html_color};')
            self.serialWasOn = True
        else:
            self.portOpenButton.setStyleSheet("background-color :  {0};".format(self.buttonColor))
            if self.serialWasOn:
                self.statusText.setText('Port died')

        # Tests for reception of json
        if (self.serialPayload.reportTimer()) > 0.2: 
            self.portStreamButton.setStyleSheet("background-color : {0};".format(self.buttonColor)) 
            self.portStreamButton.setChecked(True)
            self.serialStreamingOn = False
        else:
            html_color = self.buttonColorGenerator(frequency=.4, amplitude=0.8, phase_shift=0, hue = 0.77) 
            self.portStreamButton.setStyleSheet(f'background-color: {html_color};')
            self.portStreamButton.setChecked(False)
            self.serialStreamingOn = True

    # keypress events not handled in main are handled here
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_4:
            self.navigateWidgets(-1)
        elif key == Qt.Key_6:
            self.navigateWidgets(1)
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            f = self.widgets[self.widget_index]['function']
            f()
        else:
            super().keyPressEvent(event)

    def navigateWidgets(self, direction):
        self.widget_index = (self.widget_index + direction) % len(self.widgets)

        for i in range(len(self.widgets)):
            if i == self.widget_index:
                self.widgets[i]['widget'].setFocus()
                self.widgets[i]['widget'].setFocusPolicy(Qt.StrongFocus)
            else:
                self.widgets[i]['widget'].clearFocus()

    # attempts to open port
    def portOpen(self):
        self.sound.key_sound(self.keyPressSound[0])

        if not self.port.isOpen():
            self.port.setBaudRate( self.toolBar.baudRate() )
            self.port.setPortName( self.toolBar.portName() )
            self.port.setDataBits( 8 )
            self.port.setParity( 0 ) 
            self.port.setStopBits( 0 ) 
            self.port.setFlowControl( 0 ) 
            r = self.port.open(QtCore.QIODevice.ReadWrite)
            if not r:
                # this does not test if it is already open and happy. 
                # print ( self.toolBar.portName() )
                self.statusText.setText('Port open: error')
                self.toolBar.portOpenButton.setChecked(False)
                # self.toolBar.serialControlEnable(True)
            else:
                self.statusText.setText('Port opened')
                # self.toolBar.serialControlEnable(False)
        else:
            self.port.close()
            self.statusText.setText('Port closed')
            # self.toolBar.serialControlEnable(True)
        
    # port is open and performs a get
    def portGet(self):
        self.sound.key_sound(self.keyPressSound[0])

        if self.port.isOpen():
            text = 'get\r\n'
            self.port.write(text.encode())
        else:
            print("not open")

    # port is open and starts stream json
    def portStream(self, checked):
        self.sound.key_sound(self.keyPressSound[0])
        if self.port.isOpen():
            if checked: # then stop things
                # self.statusText.setText('Serial: no streaming')
                text = 'status stop\r\n'
            else:
                # self.statusText.setText('Serial: streaming')
                text = 'status json\r\n'
                self.serialPayload.resetTimer()
            self.port.write(text.encode())
        else:
            pass
            # self.statusText.setText('Serial: no open')

    # checks  to see if a new port/serial device is on line
    def portRefresh(self):
        self.sound.key_sound(self.keyPressSound[0])
        # self.statusText.setText('Port refresh')
        l = []
        count = 0
        for port in [ port.portName() for port in QSerialPortInfo().availablePorts() ]:
            l.append(port)
            if self.port_substring in port:
                l[count] = l[0]
                l[0] = port
            count = count + 1

        self.toolBar.portNames.clear()       
        self.toolBar.portNames.addItems( l ) 

    # among other things this loads the serial payload
    #  which is detected by parent and then loaded into
    #  UI variables`
    def readFromPort(self):
        data = self.port.readAll().data().decode()
        # strip vt100 chars
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        data = ansi_escape.sub('', data)
        data = re.sub('\| ', '\t', data)

        # get current buffer, add the data
        r = self.serialPayload.reportString() + data
        
        # Extract json strings from input buffer
        text_inside_braces = ''
        pattern = r'(\{[^}]+\}\r\n)' # find text between "{.*}\r\n"
        matches = re.findall(pattern, r) # get all matches
        text_inside_braces = ''.join(matches) # Concatenate all matches
        remaining_text = re.sub(pattern, '', r) # remove all matches

        if len(text_inside_braces) > 0:
            t = text_inside_braces.replace('\r', '')
            self.jsonDataView.appendJsonText(t, QtGui.QColor(250, 250, 250) )
            self.parent.updateJsonData(t)
            self.serialPayload.resetTimer() 

        # hoping this means we have a complete command block
        if remaining_text.endswith("@MESC>"):
            self.serialDataView.appendSerialText( remaining_text, QtGui.QColor(250, 250, 250) )
            self.parent.updateTabsWithGet()
            # print("\nstring LEN1: :: {0} :: ".format(self.serialPayload.reportString()))
            self.serialPayload.resetString()
            # print("string LEN2: :: {0} :: ".format(len(self.serialPayload.reportString())))
            r = ''
            data = ''
            remaining_text = ''
            
        self.serialPayload.setString(remaining_text)
        
    def sendFromPort(self, text):
        text = text + '\r\n'
        self.serialPayload.resetString()
        self.port.write( text.encode() )
        self.serialDataView.appendSerialText( text, QtGui.QColor(0, 0, 255) )

    # checks what type of widget it is, then adds it to our collection of widgets to help
    #   with navigating by the keys
    def linkWidget(self, w, func):
        if isinstance(w, (QtWidgets.QPushButton, QtWidgets.QCheckBox)) and callable(func):
            self.widgets[self.widget_index] = {'widget': w, 'function': func}

            if isinstance(w, QtWidgets.QPushButton):
                try:
                    w.clicked.connect(func)
                except TypeError as e:
                    print(f"Error connecting QPushButton: {e}")
            elif isinstance(w, QtWidgets.QCheckBox):
                try:
                    w.stateChanged.connect(func)
                except TypeError as e:
                    print(f"Error connecting QCheckBox: {e}")

            self.widget_index += 1
        else:
            print(f"Warning: Widget {w} or function {func} is not suitable for connection.")


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


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        
        self.buttonColor = parent.buttonColor

        self.portOpenButton = QtWidgets.QPushButton('Open')
        self.portOpenButton.setStyleSheet("background-color : {0};".format(self.buttonColor)) 
        self.portOpenButton.setCheckable(True)
        self.portOpenButton.setFixedSize(QSize(50, 50))
        parent.linkWidget(self.portOpenButton, parent.portOpen)

        self.portGetButton = QtWidgets.QPushButton('Get')
        self.portGetButton.setStyleSheet("background-color : {0};".format(self.buttonColor)) 
        self.portGetButton.setFixedSize(QSize(50, 50))
        parent.linkWidget(self.portGetButton, parent.portGet)

        self.portStreamButton = QtWidgets.QPushButton('Stream')
        self.portStreamButton.setStyleSheet("background-color : {0};".format(self.buttonColor)) 
        self.portStreamButton.setCheckable(True)
        self.portStreamButton.setFixedSize(QSize(60, 50))
        parent.linkWidget(self.portStreamButton, parent.portStream)

        self.portRefreshButton = QtWidgets.QPushButton('Refresh')
        self.portRefreshButton.setStyleSheet("background-color : {0};".format(self.buttonColor)) 
        self.portRefreshButton.setFixedSize(QSize(80, 50))
        parent.linkWidget(self.portRefreshButton, parent.portRefresh)

        self.portNames = QtWidgets.QComboBox(self)
        l = []
        count = 0
        for port in [ port.portName() for port in QSerialPortInfo().availablePorts() ]:
            l.append(port)
            if 'cu.usbmodem' in port:
                l[count] = l[0]
                l[0] = port
            count = count + 1

        self.portNames.addItems( l )
        self.portNames.setMinimumHeight(32)

        self.baudRates = QtWidgets.QComboBox(self)
        self.baudRates.addItems([
            '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', 
            '31250', '38400', '51200', '56000', '57600', '76800', '115200', '128000', '230400', '256000', '921600'
        ])
        self.baudRates.setCurrentText('115200')
        self.baudRates.setMinimumHeight(30)

        self.addWidget( self.portOpenButton )
        self.addWidget( self.portGetButton )
        self.addWidget( self.portStreamButton )
        self.addWidget( self.portRefreshButton )
        self.addWidget( self.portNames )
        self.addWidget( self.baudRates )

    def serialControlEnable(self, flag):
        self.portNames.setEnabled(flag)
        self.baudRates.setEnabled(flag)
        self.dataBits.setEnabled(flag)
        self._parity.setEnabled(flag)
        self.stopBits.setEnabled(flag)
        self._flowControl.setEnabled(flag)
        
    def baudRate(self):
        return int(self.baudRates.currentText())

    def portName(self):
        return self.portNames.currentText()


class jsonDataView(QtWidgets.QWidget):
    def __init__(self, parent):

        super(jsonDataView, self).__init__(parent)

        self.max_chars = parent.max_chars

        self.jsonData = parent.jsonData

        # self.jsonData = QtWidgets.QTextEdit(self)
        self.jsonData.setReadOnly(True)
        self.jsonData.setFontFamily('Courier New')
        self.jsonData.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setLayout( QtWidgets.QGridLayout(self) )
        self.layout().addWidget(self.jsonData, 0, 0, 1, 1)
        self.layout().setContentsMargins(2, 2, 2, 2)
        
    def appendJsonText(self, appendText, color):
        self.jsonData.moveCursor(QtGui.QTextCursor.End)
        self.jsonData.setFontFamily('Courier New')
        self.jsonData.setTextColor(color)
        current_text = self.jsonData.toPlainText()

        if len(current_text) > self.max_chars:
            # If it exceeds, truncate the text
            new_text = current_text[len(current_text)-self.max_chars:]
            self.jsonData.setPlainText(new_text)
            self.jsonData.moveCursor(QtGui.QTextCursor.End)

        self.jsonData.insertPlainText(appendText)
        self.jsonData.moveCursor(QtGui.QTextCursor.End)

class SerialDataView(QtWidgets.QWidget):
    def __init__(self, parent):

        super(SerialDataView, self).__init__(parent)

        self.port = parent.port
        self.max_chars = parent.max_chars
        self.serialData = QtWidgets.QTextEdit(self)
        self.serialData.setReadOnly(True)
        self.serialData.setFontFamily('Courier New')
        self.serialData.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setLayout( QtWidgets.QGridLayout(self) )
        self.layout().addWidget(self.serialData, 0, 0, 1, 1)
        self.layout().setContentsMargins(2, 2, 2, 2)
        
    def appendSerialText(self, appendText, color):
        self.serialData.moveCursor(QtGui.QTextCursor.End)
        self.serialData.setFontFamily('Courier New')
        self.serialData.setTextColor(color)
        current_text = self.serialData.toPlainText()

        if len(current_text) > self.max_chars:
            # If it exceeds, truncate the text
            new_text = current_text[len(current_text)-self.max_chars:]
            self.serialData.setPlainText(new_text)
            self.serialData.moveCursor(QtGui.QTextCursor.End)

        self.serialData.insertPlainText(appendText)
        self.serialData.moveCursor(QtGui.QTextCursor.End)

class SerialSendView(QtWidgets.QWidget):

    serialSendSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(SerialSendView, self).__init__(parent)

        self.port = parent.port
        self.sendData = QtWidgets.QLineEdit(self)
        self.sendData.returnPressed.connect(self.onReturnPressed)
        self.sendData.setMaximumWidth(200)
        self.sendData.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.sendButton = QtWidgets.QPushButton('Send')
        self.sendButton.clicked.connect(self.sendButtonClicked)
        self.sendButton.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        s = 'Enter string and send cmd to serial'
        if hasattr(parent, 'statusButtonHoverEnter'):
            self.sendButton.enterEvent = lambda event: parent.statusButtonHoverEnter(event, s)
        if hasattr(parent, 'statusButtonHoverLeave'):
            self.sendButton.leaveEvent = parent.statusButtonHoverLeave
        
        spacer = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.setLayout( QtWidgets.QHBoxLayout(self) )
        self.layout().addSpacerItem(spacer)
        self.layout().addWidget(self.sendData)
        self.layout().addWidget(self.sendButton)

    def onReturnPressed(self):
        text = self.sendData.text()
        text = text + '\r\n'
        self.port.write( text.encode() )
        self.sendData.clear()

    def sendButtonClicked(self):
        text = self.sendData.text()
        text = text + '\r\n'
        self.port.write( text.encode() )
        self.sendData.clear()

