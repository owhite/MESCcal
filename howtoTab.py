import sys
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy, QTextBrowser
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

### Tab that handles acknowledgements
###   toubleshooting and links to additional information

class howtoTab(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setCentralWidget(QtWidgets.QWidget(self))
        tab_layout = QtWidgets.QVBoxLayout(self.centralWidget())

        file_path = "howto.html"

        # Read HTML content from the file
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Create a QLabel to display the text
        label = QtWidgets.QLabel(self)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        label.setText(text)

        # Create a QScrollArea and set the QLabel as its widget
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidget(label)
        scroll_area.setWidgetResizable(True)
        scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        tab_layout.addWidget(scroll_area)

    def open_link(self, url):
        # Opens the user's default web browser
        QtGui.QDesktopServices.openUrl(QtGui.QUrl(url))

