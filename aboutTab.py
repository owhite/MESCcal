import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy
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

        text = """
        <div style="text-align: left;">
        <H2 style="text-align:center;">mescaline</H2>
        <H3>Introduction</H3>
        <br>
        mescaline is a companion tool for the 
        <a href="https://github.com/davidmolony/MESC_Firmware">MESC_firmware 
        project</a> written by David Molony; many thanks to him for 
        his patience and help with the MESC code. 
        <br>
        <br>
        I would also like to acknowledge the tremendous 
        work of <a href="https://github.com/Netzpfuscher">Netzpfuscher</a> for his development
        of the MESC_Firmware serial terminal. 
        <br>
        <br>
        An instructional video on the use of this mescaline can be found here: 
        [<a href="https://youtu.be/dQw4w9WgXcQ?t=43">LINK</a>].
        <br>
        <H3>Troubleshooting</H3>
        <br>
        <b>Serial connection.</b>The PYQT5 environment that does serial handling is very stable. If you're having 
        trouble connecting it probably does not have to do with the interface. If you can't connect to the serial try:
        <ul style="list-style-type: disc;">
        <li>Connecting the MESC board to your computer and THEN powering up the MESC board
        <li>Checking to see if your computer sees a new port 
        <li>Using a different terminal program (for Macs and Linux: screen, Windows: minicom)
        </ul>
        If you can't view the MESC board through your serial using another terminal program you are not
        likely to get it to work on mescaline either. 
        </div>

        """

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

