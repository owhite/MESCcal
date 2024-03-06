import sys
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy, QTextBrowser
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

### Tab that handles acknowledgements
###   toubleshooting and links to additional information

class aboutTab(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.keyPressSound = parent.keyPressSound
        self.useKeypresses = parent.useKeypresses
        self.port = parent.port
        self.initUI()

    def initUI(self):
        self.big_font = QtGui.QFont()
        self.mid_font = QtGui.QFont()
        self.smol_font = QtGui.QFont()

        self.checkboxes = {}
        self.widgets = []
        self.widget_index = 0

        self.big_font.setPointSize(16)
        self.mid_font.setPointSize(14)
        self.smol_font.setPointSize(12)

        self.setCentralWidget(QtWidgets.QWidget(self))

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget(scroll_area)

        main_layout = QtWidgets.QVBoxLayout(scroll_content)
        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        main_layout.setContentsMargins(20, 3, 200, 3)
        main_layout.addLayout(layout)

        layout.addWidget(self.titleBox())
        layout.addWidget(self.preferencesBox())

        self.saveButton = QtWidgets.QPushButton('Save')
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.saveButton.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        layout.addWidget(self.saveButton)

        scroll_area.setWidget(scroll_content)
        self.setCentralWidget(scroll_area)

    def saveButtonClicked(self):
        pass

    def preferencesBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setStyleSheet("QGroupBox { border: 1px solid white; }")

        layout = QtWidgets.QVBoxLayout()

        combined_layout = QtWidgets.QHBoxLayout()

        # Create the first QVBoxLayout for radio buttons
        layout1 = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Set MESCcal UI preferences")
        label.setFont(self.big_font)
        layout1.addWidget(label)

        self.checkBoxRow(layout1, self.keyPressSound, 'Play key press sounds')
        combined_layout.addLayout(layout1)

        self.checkBoxRow(layout1, self.useKeypresses, 'Use gameboy keys')
        layout.addLayout(combined_layout)

        box.setLayout(layout)

        return box

    def checkBoxRow(self, layout, mutable, label_text):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(10)

        # Create a QCheckBox
        cb = QtWidgets.QCheckBox('')
        cb.setChecked(mutable[0])
        cb.stateChanged.connect(self.onCheckboxChange)

        self.checkboxes[cb] = {}
        self.checkboxes[cb]['value'] = mutable
        self.widgets.append(cb)
        self.widget_index += 1

        cb.setFont(self.smol_font)
        row.addWidget(cb)
        
        label = QtWidgets.QLabel(label_text)
        label.setFont(self.smol_font)
        label.setAlignment(QtCore.Qt.AlignRight)
        row.setAlignment(QtCore.Qt.AlignLeft)
        row.addWidget(label)

        layout.addLayout(row)

    def onCheckboxChange(self):
        cb = self.sender()
        self.checkboxes[cb]['value'][0] = cb.isChecked()
        print(cb.isChecked())

    def intFloatOrNone(self, s):
        if s == "None":
            return(None)
        if s is None:
            return(None)

        sign = 1
        if s.startswith('-'):
            sign = -1
            s = re.sub('^-', '', s)

        if s.isdigit():
            s = int(s)
        else:
            s = float(s)

        return(s * sign)


    def titleBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        # box.setFixedHeight(220) # I dislike this is the only way to control space around text
        box.setStyleSheet("QGroupBox { border: 3px solid white; }")
        # Create the first QVBoxLayout for radio buttons
        layout = QtWidgets.QVBoxLayout()

        text = """
        <div style="text-align: left;">
        <H2 style="text-align:center;">About MESCcal: the MESC calibration tool</H2>
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
        </div>
        """

        # Create a QLabel to display the text
        label = QtWidgets.QLabel(self)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        label.setText(text)
        layout.addWidget(label)
        box.setLayout(layout)

        return box

    def open_link(self, url):
        # Opens the user's default web browser
        QtGui.QDesktopServices.openUrl(QtGui.QUrl(url))

