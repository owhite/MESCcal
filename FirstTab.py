import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# Port connection tab -- handles serial connection and sending commands

class FirstTab(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.port = parent.port
        self.statusText = parent.statusText
        self.getButton = parent.getButton
        self.saveButton = parent.saveButton
        self.tButton = parent.getButton
        self.serialStreamingOn = parent.serialStreamingOn
        self.serialCMDOn = parent.serialCMDOn
        self.serialPayload = parent.serialPayload
        self.max_chars = 3000

        self.initUI()

    def initUI(self):
        self.serialDataView = SerialDataView(self)
        self.serialSendView = SerialSendView(self)

        self.setCentralWidget( QtWidgets.QWidget(self) )

        layout = QtWidgets.QVBoxLayout( self.centralWidget() )
        layout.addWidget(self.serialDataView)
        layout.addWidget(self.serialSendView)
        layout.setContentsMargins(3, 3, 3, 3)

        ### Tool Bar ###
        self.toolBar = ToolBar(self)
        self.addToolBar(self.toolBar)
        
        ### Signal Connect ###
        self.toolBar.portOpenButton.clicked.connect(self.portOpen)
        self.toolBar.portRefreshButton.clicked.connect(self.portRefresh)
        self.serialSendView.serialSendSignal.connect(self.sendFromPort)
        self.port.readyRead.connect(self.readFromPort)

    def portOpen(self, flag):
        if flag:
            self.port.setBaudRate( self.toolBar.baudRate() )
            self.port.setPortName( self.toolBar.portName() )
            self.port.setDataBits( 8 )
            self.port.setParity( 0 ) 
            self.port.setStopBits( 0 ) 
            self.port.setFlowControl( 0 ) 
            r = self.port.open(QtCore.QIODevice.ReadWrite)
            if not r:
                # this does not test if it is already open and happy. 
                print ( self.toolBar.portName() )
                self.statusText.setText('Port open: error')
                # self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
                # self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
                self.toolBar.portOpenButton.setChecked(False)
                # self.toolBar.serialControlEnable(True)
            else:
                # self.getButton.setStyleSheet("background-color : green;" "border :1px solid green;") 
                # self.saveButton.setStyleSheet("background-color : green;" "border :1px solid green;") 
                self.statusText.setText('Port opened')
                # self.toolBar.serialControlEnable(False)
        else:
            self.port.close()
            # self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            # self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;") 
            self.statusText.setText('Port closed')
            # self.toolBar.serialControlEnable(True)
        
    def portRefresh(self, flag):
        self.port.close() # bad idea? 
        self.portOpen(True)
        self.statusText.setText('Port refresh')
        l = []
        count = 0
        for port in [ port.portName() for port in QSerialPortInfo().availablePorts() ]:
            l.append(port)
            if 'cu.usbmodem' in port:
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
        self.serialPayload.resetTimer()

        self.serialPayload.concatString(data)
        r = self.serialPayload.reportString()
        if self.parent.serialCMDOn:
            if "@MESC>" in r:

                print("{0} :: {1}".format(self.parent.serialCMDOn, r))
                self.parent.serialCMDOn = False
                self.serialPayload.resetString()

        if len(data) > 0:
            self.serialDataView.appendSerialText( data, QtGui.QColor(0, 0, 0) )

    def sendFromPort(self, text):
        text = text + '\r\n'
        self.serialPayload.resetString()
        self.port.write( text.encode() )
        self.serialPayload.resetTimer()
        self.serialDataView.appendSerialText( text, QtGui.QColor(0, 0, 255) )


class SerialDataView(QtWidgets.QWidget):
    def __init__(self, parent):

        super(SerialDataView, self).__init__(parent)

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

        self.sendData = QtWidgets.QTextEdit(self)
        self.sendData.setAcceptRichText(False)
        self.sendData.setMaximumHeight(32)
        self.sendData.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.sendButton = QtWidgets.QPushButton('Send')
        self.sendButton.clicked.connect(self.sendButtonClicked)
        self.sendButton.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        
        self.setLayout( QtWidgets.QHBoxLayout(self) )
        self.layout().addWidget(self.sendData)
        self.layout().addWidget(self.sendButton)
        self.layout().setContentsMargins(3, 3, 3, 3)


    def sendButtonClicked(self):
        self.serialSendSignal.emit( self.sendData.toPlainText() )
        self.sendData.clear()

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        
        self.portOpenButton = QtWidgets.QPushButton('Open')
        self.portOpenButton.setCheckable(True)
        self.portOpenButton.setMinimumHeight(32)

        self.portRefreshButton = QtWidgets.QPushButton('Refresh')
        # self.portRefreshButton.setCheckable(True)
        self.portRefreshButton.setMinimumHeight(32)

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

