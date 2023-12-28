import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTextBrowser, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QCheckBox, QLabel, QDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl

### Tab that handles acknowledgements
###   toubleshooting and links to additional information

class aboutTab(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setCentralWidget(QtWidgets.QWidget(self))
        tab_layout = QtWidgets.QVBoxLayout(self.centralWidget())

    def updateThisTab(self):
        dialog = aboutDialog()
        dialog.exec_()

    def open_link(self, url):
        # Opens the user's default web browser
        QtGui.QDesktopServices.openUrl(QtGui.QUrl(url))

class aboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        text = """
        <div style="text-align: left;">
        <H2 style="text-align:center;">MESCcal: the MESC calibration tool</H2>
        <H3></H3>
        <br>
        MESCcal is a calibration tool for the 
        <a href="https://github.com/davidmolony/MESC_Firmware" style="color: #F39C12;">MESC_firmware 
        project</a> written by David Molony; many thanks to him for 
        his patience and help with the MESC code. 
        <br>
        <br>
        I would also like to acknowledge the tremendous 
        work of <a href="https://github.com/Netzpfuscher" style="color: #F39C12;">Netzpfuscher</a> for his development
        of the MESC_Firmware serial terminal. 
        <br>
        <br>
        An instructional video on the use of MESCcal can be found here: 
        [<a href="https://youtu.be/dQw4w9WgXcQ?t=43" style="color: #F39C12;">LINK</a>].
        <br>
        <br>
        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; -owen
        </div>
        """

        # Use QTextBrowser instead of QLabel for clickable links
        text_browser = QTextBrowser(self)
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml(text)

        vbox.addWidget(text_browser)

        close_button = QtWidgets.QPushButton('Okay', self)
        close_button.clicked.connect(self.close)
        vbox.addWidget(close_button)

        self.setLayout(vbox)
        self.setWindowTitle('About MESCcal')
        self.setGeometry(180, 300, 460, 350)

        # Connect the open_link method to the anchorClicked signal
        text_browser.anchorClicked.connect(self.open_link)

    def open_link(self, url):
        # Opens the user's default web browser
        QDesktopServices.openUrl(url)
