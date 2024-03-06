import sys
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy, QTextBrowser
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

### Tab that handles preferencs

class speedoPrefs(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.keyPressSound = parent.keyPressSound
        self.useKeypresses = parent.useKeypresses
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

        label = QtWidgets.QLabel("Set UI preferences")
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



