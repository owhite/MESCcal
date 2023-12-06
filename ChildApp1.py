from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton

class ChildApp1(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def initUI(self):
        self.setWindowTitle('New Window')
        self.label_received_data = QtWidgets.QLabel('No data received yet', self)
        label = QtWidgets.QLabel('This is the second window', self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)

        self.setLayout(layout)
        self.setGeometry(200, 200, 400, 200)

    def receive_data(self, data):
        self.label_received_data.setText(f'Received data: {data}')

