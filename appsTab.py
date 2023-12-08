import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# Handles displaying all the apps that are available to the user
class appsTab(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.classes_found = parent.classes_found
        self.module_directory = parent.module_directory
        self.port = parent.port
        self.loadModules = parent.loadModules.load
        self.killWindow = parent.loadModules.killWindow
        self.windowNames = parent.loadModules.windowNames

        self.initUI()

    def initUI(self):
        ### Tool Bar ###
        self.toolBar = self.addToolBar('APPS')
        self.portRefreshButton = QtWidgets.QPushButton('Refresh')
        self.portRefreshButton.setMinimumHeight(32)
        self.portRefreshButton.clicked.connect(self.appRefresh)
        self.toolBar.addWidget( self.portRefreshButton )
        self.addToolBar(self.toolBar)
        
        self.setCentralWidget( QtWidgets.QWidget(self) )
        layout = QtWidgets.QVBoxLayout( self.centralWidget() )
        layout.setAlignment(Qt.AlignTop) 

        # this list reflects potental apps to load
        #  self.windowNames is a list of the ones that HAVE been loaded
        classes = [re.sub(r'.*\/', '', item) for item in self.classes_found]
        classes = [re.sub(r'.py', '', item) for item in classes]
        
        # List to hold references to push buttons
        self.buttons = []

        # Create push buttons using a for loop
        for name in self.classes_found.keys():
            push_button = QtWidgets.QPushButton(name)
            push_button.setFixedWidth(200)
            push_button.setStyleSheet("background-color : white;" "border :1px solid black;")
            push_button.setCheckable(True)
            self.buttons.append(push_button)
            layout.addWidget(push_button)

        # Connect the clicked signal to a slot function
        for button in self.buttons:
            button.clicked.connect(self.on_button_clicked)

        layout.setContentsMargins(3, 3, 3, 3)

    def on_button_clicked(self, button):
        sender_button = self.sender()
        name = sender_button.text()
        if sender_button.isChecked():
            sender_button.setStyleSheet("background-color : lightblue;" "border :1px solid black;")
            print('run: {0} :: {1}'.format(name, self.classes_found[name]))
            self.loadModules([self.classes_found[name]])
        else:
            sender_button.setStyleSheet("background-color : white;" "border :1px solid black;")
            print('stop: {0} :: {1}'.format(name, self.classes_found[name]))
            self.killWindow(name)

        QTimer.singleShot(100, lambda: None)

    # To do, perform a refresh on the list of available apps
    def appRefresh(self, flag):
        print(self.windowNames)


