import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

### Tab that handles displaying all the apps that are available to the user
###    that are available to the user for launching
###    
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.checkAppStatus("beep"))
        self.timer.start(100)

        # this list reflects potental apps to load
        #  self.windowNames is a list of the ones that HAVE been loaded
        classes = [re.sub(r'.*\/', '', item) for item in self.classes_found]
        classes = [re.sub(r'.py', '', item) for item in classes]
        
        # List to hold references to push buttons
        self.buttons = {}

        # Create push buttons using a for loop
        for name in self.classes_found.keys():
            push_button = QtWidgets.QPushButton(name)
            push_button.setFixedWidth(200)
            push_button.setStyleSheet("background-color : white;" "border :1px solid black;")
            push_button.setCheckable(True)
            self.buttons[name] = push_button
            layout.addWidget(push_button)
            push_button.clicked.connect(self.on_button_clicked)

        # Connect the clicked signal to a slot function

        layout.setContentsMargins(3, 3, 3, 3)

    # needed in case the user closes the window outside of the main app
    def checkAppStatus(self, w): 
        for name in self.classes_found.keys():
            pb = self.buttons[name]
            if name in self.windowNames:
                pb.setStyleSheet("background-color : lightblue;" "border :1px solid black;")
                pb.setChecked(True)
            else:
                pb.setStyleSheet("background-color : white;" "border :1px solid black;")
                pb.setChecked(False)

    def on_button_clicked(self, button):
        sender_button = self.sender()
        name = sender_button.text()
        if sender_button.isChecked():
            self.loadModules([self.classes_found[name]])
        else:
            self.killWindow(name)

        QTimer.singleShot(100, lambda: None)

    # To do, perform a refresh on the list of available apps
    def appRefresh(self, flag):
        print(self.windowNames)


