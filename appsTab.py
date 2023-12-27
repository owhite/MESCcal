import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from functools import partial

### Tab that handles displaying all the apps that are available to the user
###    that are available to the user for launching
###    
class appsTab(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.classes_found = parent.classes_found
        self.modules_dict = parent.modules_dict
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

        for name in self.classes_found.keys():
            row_layout = QtWidgets.QHBoxLayout()
            row_layout.setSpacing(1)

            pb = QtWidgets.QPushButton('GO')
            pb.setFixedWidth(40)
            # pb.setStyleSheet("background-color : white;" "border :1px solid black;")
            pb.setCheckable(True)
            pb.clicked.connect(partial(self.on_button_clicked, name))

            self.buttons[name] = pb
            row_layout.addWidget(pb)

            app_desc = 'No description'
            app_name = name
            if self.modules_dict.get(name):
                d = self.modules_dict.get(name)
                if d.get('app_name'):
                    app_name = d['app_name']
                if d.get('app_desc'):
                    app_desc = d['app_desc']

            app_name = " :: " + app_name
            label1 = QtWidgets.QLabel(app_name) 
            label1.setFixedWidth(140)
            row_layout.addWidget(label1)

            label2 = QtWidgets.QLabel(app_desc)
            label2.setFixedWidth(600)
            row_layout.addWidget(label2)

            layout.addLayout(row_layout)

        # Connect the clicked signal to a slot function

        layout.setContentsMargins(3, 3, 3, 3)

    def on_button_clicked(self, name):
        sender_button = self.sender()

        if sender_button.isChecked():
            self.loadModules([self.modules_dict['dict'][name]])
        else:
            self.killWindow(name)

        QTimer.singleShot(100, lambda: None)

    # needed in case the user closes the window outside of the main app
    def checkAppStatus(self, w): 
        for name in self.classes_found.keys():
            pb = self.buttons[name]
            if name in self.windowNames:
                # pb.setStyleSheet("background-color : lightblue;" "border :1px solid black;")
                pb.setChecked(True)
            else:
                # pb.setStyleSheet("background-color : white;" "border :1px solid black;")
                pb.setChecked(False)

    # To do, perform a refresh on the list of available apps
    def appRefresh(self, flag):
        print(self.windowNames)


