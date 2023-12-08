import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl

# Handles displaying all the apps that are available to the user
class aboutTab(QtWidgets.QMainWindow): 

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        ### Tool Bar ###
        self.toolBar = self.addToolBar('APPS')
        self.addToolBar(self.toolBar)

        self.setCentralWidget( QtWidgets.QWidget(self) )
        layout = QtWidgets.QVBoxLayout( self.centralWidget() )

        # Create a QTextBrowser with a clickable link


        text = """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            This is an example of a hotlink. Click <a href="http://www.google.com">here</a> to open the website in your browser.
            This is another line in the text.
            This is a new line with a line break.<br>
            And another line after the line break.
        </div>
        """

        text = """
        <div style="text-align: center;">
            This is an example of a hotlink. Click <a href="http://www.google.com">here</a> to open the website in your browser.
            This is another line in the text.
            This is a new line with a line break.<br>
            And another line after the line break.
        </div>
        """

        self.text_browser = QtWidgets.QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setHtml(text)
        self.text_browser.anchorClicked.connect(self.open_link)

        layout.addWidget(self.text_browser)

    def open_link(self, url):
        # Open the link in the user's default web browser
        QDesktopServices.openUrl(QUrl(url))

