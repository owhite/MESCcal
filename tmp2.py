#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QVBoxLayout, QWidget
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class TextDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Text Display Example')

        # Create a QTextBrowser with a clickable link
        text = """
        This is an example of a hotlink. Click <a href="http://www.google.com">here</a> to open the website in your browser.
        """

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setHtml(text)
        self.text_browser.anchorClicked.connect(self.open_link)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_link(self, link):
        # Open the link in the user's default web browser
        QDesktopServices.openUrl(QUrl(link.toString()))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = TextDisplayWindow()
    main_window.show()

    sys.exit(app.exec_())
