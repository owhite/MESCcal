import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QCheckBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtGui import QFont  # Import QFont from QtGui
from functools import partial
import colorsys
import ColorSegmentRing

### Presets tab -- provides user with simple methods to turn motor
###
class presetsTab(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.port = parent.port
        self.statusText = parent.statusBar.statusText
        self.customButtonHoverEnter = parent.statusBar.customButtonHoverEnter
        self.customButtonHoverLeave = parent.statusBar.customButtonHoverLeave
        self.dataEntryButtonClicked = parent.dataEntryButtonClicked
        self.initUI()

    def initUI(self):
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(18)

        self.mid_font = QtGui.QFont()
        self.mid_font.setPointSize(14)

        self.smol_font = QtGui.QFont()
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
        layout.addWidget(self.openLoopBox())
        layout.addWidget(self.throttleBox())

        scroll_area.setWidget(scroll_content)
        self.setCentralWidget(scroll_area)

    def throttleBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setStyleSheet("QGroupBox { border: 1px solid black; }")

        layout = QtWidgets.QVBoxLayout()

        combined_layout = QtWidgets.QHBoxLayout()
        combined_layout.setSpacing(0)

        # Create the first QVBoxLayout for radio buttons
        layout1 = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Throttle test')
        label.setFont(self.big_font)
        layout1.addWidget(label)

        self.checkBoxRow(layout1, 'set curr_max 40', '', '(40 Amps, something safe)')
        self.checkBoxRow(layout1, 'set motor_sensor 0', '', '(0 = SL, "sensorless")')
        self.checkBoxRow(layout1, 'status json', 'status stop', '(stream variables to status bar)')
        self.checkBoxRow(layout1, 'set input_opt 1', 'set input_opt 8', '(checked sets to 1 = ADC1, unchecked sets 8 = UART )')
        self.setValueRow(layout1, 'adc1_min', 'set adc1_min')
        self.setValueRow(layout1, 'adc1_max', 'set adc1_max')

        # Create the second QVBoxLayout
        layout2 = QtWidgets.QVBoxLayout()
        # decided not to do this. 
        # self.adc1_ring = ColorSegmentRing.colorSegmentRing()
        # self.adc1_ring.setVisible(True)
        # self.adc1_ring.ring_text = 'adc1'
        # self.adc1_ring.ring_text_size = 16
        # layout2.addWidget(self.adc1_ring)

        combined_layout.addLayout(layout1)
        combined_layout.addLayout(layout2)

        layout.addLayout(combined_layout)

        label = QtWidgets.QLabel("Physically connect a potentiometer to the adc1 input of your mesc board.  Once you have selected \"status json\" you should see the throttle widget updating when you turn your potentiometer.  Change the set input_opt value to 1 to send adc1 values to your controller.")

        label.setFont(self.smol_font)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        layout.addWidget(label)
        box.setLayout(layout)

        return box

    def openLoopBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setStyleSheet("QGroupBox { border: 1px solid black; }")

        layout = QtWidgets.QVBoxLayout()

        combined_layout = QtWidgets.QHBoxLayout()

        # Create the first QVBoxLayout for radio buttons
        layout1 = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Run in open loop')
        label.setFont(self.big_font)
        layout1.addWidget(label)

        label = QtWidgets.QLabel("Running in open loop mode turns the motor with no feedback control.")
        label.setFont(self.smol_font)
        layout1.addWidget(label)

        self.checkBoxRow(layout1, 'set curr_max 40', '', '(40 Amps, something safe)')
        self.checkBoxRow(layout1, 'set input_opt 8', '', '(8 = UART,  meaning: receive control input from UART)')
        self.checkBoxRow(layout1, 'set motor_sensor 2', '', '(2 = open loop)')
        self.checkBoxRow(layout1, 'set ol_step 20', '', '(number of steps per pulse)')
        self.checkBoxRow(layout1, 'status json', 'status stop', '(stream variables to status bar)')
        self.checkBoxRow(layout1, 'set uart_req 10', 'set uart_req 0', '(requesting 10 Amps,  uncheck to stop)')

        # Create the second QVBoxLayout
        layout2 = QtWidgets.QVBoxLayout()
        row = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('')
        label.setFont(self.smol_font)
        row.addWidget(label)
        layout2.addLayout(row)

        combined_layout.addLayout(layout1)
        combined_layout.addLayout(layout2)

        layout.addLayout(combined_layout)

        label = QtWidgets.QLabel("Selecting these click boxes should get your motor spinning.  status json is optional but it will show some interesting results in the status bar. To stop,  unselect the last checkbox.  If the motor is attempting to spin or not spinning check your wiring and controller.  If it's a large motor you may need to set curr_max to something > 40 Amps.")
        label.setFont(self.smol_font)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        layout.addWidget(label)
        box.setLayout(layout)

        return box

    def titleBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setFixedHeight(190) # I dislike this is the only way to control space around text
        box.setStyleSheet("QGroupBox { border: 2px solid black; }")
        # Create the first QVBoxLayout for radio buttons
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Interactive presets for testing and operation')
        label.setFont(self.big_font)
        layout.addWidget(label)

        label = QtWidgets.QLabel('Use these presets to learn how to run the MESC controller.  Each block of checkboxes shows you how you which values to set in order to get the controller to do something.  When you select each checkbox it will send the listed command to the serial.  The serial port must be open to start and you may want to stream data to update the status bar by selecting the Data button.  If you like your settings select the "set" button to save your parameters.')
        label.setFont(self.mid_font)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        layout.addWidget(label)

        label = QtWidgets.QLabel('Caution: remove obstructions around you motor and be ready for it to turn.')
        label.setFont(self.mid_font)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        layout.addWidget(label)

        box.setLayout(layout)

        return box

    def setValueRow(self, layout, mesc_value, label_text):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(10)

        entry_item = QtWidgets.QLineEdit()
        entry_item.setFixedWidth(60)
        entry_item.setMinimumHeight(22)

        pb = QtWidgets.QPushButton(mesc_value)
        pb.setFixedWidth(100)
        pb.setMinimumHeight(12)
        pb.setToolTip("set the minimum value range for adc1")
        pb.clicked.connect(partial(self.dataEntryButtonClicked, mesc_value, entry_item))
        row.addWidget(pb)
        
        row.addWidget(entry_item)

        label = QtWidgets.QLabel(label_text)
        label.setFont(self.smol_font)
        label.setAlignment(QtCore.Qt.AlignLeft)
        row.setAlignment(QtCore.Qt.AlignLeft)
        row.addWidget(label)

        layout.addLayout(row)

    def checkBoxRow(self, layout, start_text, stop_text, label_text):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(10)

        # Create a QCheckBox
        cb = QtWidgets.QCheckBox('')
        cb.stateChanged.connect(lambda state: self.onCheckboxChange(state, start_text, stop_text))
        cb.setFont(self.smol_font)
        row.addWidget(cb)
        
        # Create a QLabel with left alignment
        label = QtWidgets.QLabel(start_text + " " + label_text)
        label.setFont(self.smol_font)
        label.setAlignment(QtCore.Qt.AlignRight)  # Set left alignment
        row.setAlignment(QtCore.Qt.AlignLeft)
        row.addWidget(label)

        layout.addLayout(row)

    def onCheckboxChange(self, state, start, stop):
        if state == 2:
            text = start + '\r\n'
        else:
            text = stop + '\r\n'

        self.port.write( text.encode() )
