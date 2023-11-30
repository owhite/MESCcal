import re
from PyQt6 import QtWidgets, QtCore, QtGui, QtSerialPort
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTabWidget, QTextEdit, QFormLayout, QGridLayout, QComboBox, QHBoxLayout, QToolBar
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtGui import QColor

class FirstTab(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.port = parent.port
        self.statusText = parent.statusText
        self.getButton = parent.getButton
        self.saveButton = parent.saveButton
        self.tButton = parent.getButton
        self.serialPayload = parent.serialPayload

        self.initUI()

    def initUI(self):
        self.serialDataView = SerialDataView(self)
        self.serialSendView = SerialSendView(self)

        self.setCentralWidget(QWidget(self))

        layout = QVBoxLayout(self.centralWidget())
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
            self.port.setBaudRate(self.toolBar.baudRate())
            self.port.setPortName(self.toolBar.portName())

            r = self.port.open(QSerialPort.OpenModeFlag.ReadWrite)
            if not r:
                print(self.toolBar.portName())
                self.statusText.setText('Port open: error')
                self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;")
                self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;")
                self.toolBar.portOpenButton.setChecked(False)
            else:
                self.getButton.setStyleSheet("background-color : green;" "border :1px solid green;")
                self.saveButton.setStyleSheet("background-color : green;" "border :1px solid green;")
                self.statusText.setText('Port opened')
        else:
            self.port.close()
            self.getButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;")
            self.saveButton.setStyleSheet("background-color : yellow;" "border :1px solid yellow;")
            self.statusText.setText('Port closed')

    def portRefresh(self, flag):
        self.port.close()
        self.portOpen(True)
        self.statusText.setText('Port refresh')
        l = []
        count = 0
        for port in [port.portName() for port in QSerialPortInfo().availablePorts()]:
            l.append(port)
            if 'cu.usbmodem' in port:
                l[count] = l[0]
                l[0] = port
            count = count + 1

        self.toolBar.portNames.clear()
        self.toolBar.portNames.addItems(l)

    def readFromPort(self):
        data = self.port.readAll().data().decode()
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        data = ansi_escape.sub('', data)
        data = re.sub('\| ', '\t', data)
        self.serialPayload.resetTimer()
        self.serialPayload.concatString(data)

        if len(data) > 0:
            self.serialDataView.appendSerialText(data, QColor(0, 0, 0))

    def sendFromPort(self, text):
        text = text + '\r\n'
        self.serialPayload.resetString()
        self.port.write(text.encode())
        self.serialPayload.resetTimer()
        self.serialDataView.appendSerialText(text, QColor(0, 0, 255))


from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTabWidget, QTextEdit, QFormLayout, QGridLayout, QComboBox, QHBoxLayout, QToolBar
from PyQt6.QtGui import QColor, QTextCursor

class SerialDataView(QWidget):
    def __init__(self, parent):
        super(SerialDataView, self).__init__(parent)

        self.serialData = QTextEdit(self)
        self.serialData.setReadOnly(True)
        self.serialData.setFontFamily('Courier New')
        self.setLayout(QGridLayout(self))
        self.layout().addWidget(self.serialData, 0, 0, 1, 1)
        self.layout().setContentsMargins(2, 2, 2, 2)

    def appendSerialText(self, appendText, color):
        self.text_edit = QTextEdit().textCursor().End()
        self.serialData.setFontFamily('Courier New')
        self.serialData.setTextColor(color)
        self.serialData.insertPlainText(appendText)
        self.text_edit = QTextEdit().textCursor().End()


class SerialSendView(QWidget):

    serialSendSignal = pyqtSignal(str)
    def __init__(self, parent):
        super(SerialSendView, self).__init__(parent)

        self.sendData = QTextEdit(self)
        self.sendData.setAcceptRichText(False)
        self.sendData.setMaximumHeight(32)

        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.sendButtonClicked)

        self.setLayout(QHBoxLayout(self))
        self.layout().addWidget(self.sendData)
        self.layout().addWidget(self.sendButton)
        self.layout().setContentsMargins(3, 3, 3, 3)

    def sendButtonClicked(self):
        self.serialSendSignal.emit(self.sendData.toPlainText())
        self.sendData.clear()


class ToolBar(QToolBar):
    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)

        self.portOpenButton = QPushButton('Open')
        self.portOpenButton.setCheckable(True)
        self.portOpenButton.setMinimumHeight(32)

        self.portRefreshButton = QPushButton('Refresh')
        self.portRefreshButton.setCheckable(True)
        self.portRefreshButton.setMinimumHeight(32)

        self.portNames = QComboBox(self)
        l = []
        count = 0
        for port in [port.portName() for port in QSerialPortInfo().availablePorts()]:
            l.append(port)
            if 'cu.usbmodem' in port:
                l[count] = l[0]
                l[0] = port
            count = count + 1

        self.portNames.addItems(l)
        self.portNames.setMinimumHeight(32)

        self.baudRates = QComboBox(self)
        self.baudRates.addItems([
            '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800',
            '31250', '38400', '51200', '56000', '57600', '76800', '115200', '128000', '230400', '256000', '921600'
        ])
        self.baudRates.setCurrentText('115200')
        self.baudRates.setMinimumHeight(30)

        self.addWidget(self.portOpenButton)
        self.addWidget(self.portRefreshButton)
        self.addWidget(self.portNames)
        self.addWidget(self.baudRates)

    def serialControlEnable(self, flag):
        self.portNames.setEnabled(flag)
        self.baudRates.setEnabled

    def baudRate(self):
        return int(self.baudRates.currentText())

    def portName(self):
        return self.portNames.currentText()
