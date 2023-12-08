import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# Port connection tab -- handles serial connection and sending commands

class appsTab(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.classes_found = parent.classes_found
        self.windows = parent.windows
        self.module_directory = parent.module_directory
        self.port = parent.port
        self.loadModules = parent.loadModules.load

        self.initUI()

    def initUI(self):
        # This allows you to see all the json streaming which is fine for debugging
        #   but not really needed for operation

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

        classes = [re.sub(r'.*\/', '', item) for item in self.classes_found]
        classes = [re.sub(r'.py', '', item) for item in classes]
        self.buttons = {}
        
        # List to hold references to push buttons
        self.buttons = []

        # Create push buttons using a for loop
        for name in self.classes_found.keys():
            push_button = QtWidgets.QPushButton(name)
            push_button.setCheckable(True)
            self.buttons.append(push_button)
            layout.addWidget(push_button)

        # Connect the clicked signal to a slot function
        for button in self.buttons:
            button.clicked.connect(self.on_button_clicked)

        layout.setContentsMargins(3, 3, 3, 3)

    def on_button_clicked(self, button):
        sender_button = self.sender()
        if sender_button.isChecked():
            name = sender_button.text()
            print('run: {0} :: {1}'.format(name, self.classes_found[name]))
            self.windows = self.loadModules(self.module_directory, [self.classes_found[name]])
            print("HERE")
            print(self.windows)
        else:
            print(self.windows)
            print('stop: {0} :: {1}'.format(name, self.classes_found[name]))

    def updateButtons(self, checked):
        # Toggle the visibility of the QTextEdit based on the radio button state
        pass

    def appRefresh(self, flag):
        pass

