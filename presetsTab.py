import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QCheckBox, QLabel, QDialog
from PyQt5.QtCore import Qt, QTimer
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
        self.os = parent.os
        self.statusText = parent.statusBar.statusText
        self.customButtonHoverEnter = parent.statusBar.customButtonHoverEnter
        self.customButtonHoverLeave = parent.statusBar.customButtonHoverLeave
        self.dataEntryButtonClicked = parent.dataEntryButtonClicked
        self.initUI()

    def initUI(self):
        self.big_font = QtGui.QFont()
        self.mid_font = QtGui.QFont()
        self.smol_font = QtGui.QFont()

        self.checkboxes = {}
        self.entryboxes = {}
        self.programmatic_change = False

        self.timer = QTimer(self)

        self.big_font.setPointSize(16)
        self.mid_font.setPointSize(14)
        self.smol_font.setPointSize(12)

        if self.os == 'Win':
            self.big_font.setPointSize(14)
            self.mid_font.setPointSize(12)
            self.smol_font.setPointSize(10)

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
        layout.addWidget(self.uartreqBox())

        scroll_area.setWidget(scroll_content)
        self.setCentralWidget(scroll_area)

    # goal: whenever tab is opened, or user makes a change to a preset value
    #  update the status of all the radio buttons, etc. 
    def updateThisTab(self):
        if not self.port.isOpen():
            self.showDialog()
            return()
        else:
            text = 'get\r\n'
            self.port.write( text.encode() )
        
    def setValueRow(self, layout, mesc_value, label_text, tooltip):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(10)

        entry_item = QtWidgets.QLineEdit()
        entry_item.setFixedWidth(60)
        entry_item.setMinimumHeight(28)

        self.entryboxes[entry_item] = mesc_value

        pb = QtWidgets.QPushButton(mesc_value)
        pb.setFixedWidth(100)
        pb.setMinimumHeight(12)
        pb.setToolTip(tooltip)
        pb.clicked.connect(partial(self.dataEntryButtonClicked, mesc_value, entry_item))
        row.addWidget(pb)
        
        row.addWidget(entry_item)

        label = QtWidgets.QLabel(label_text)
        label.setFont(self.smol_font)
        label.setAlignment(QtCore.Qt.AlignLeft)
        row.setAlignment(QtCore.Qt.AlignLeft)
        row.addWidget(label)

        layout.addLayout(row)

    def checkBoxRow(self, layout, name, start, stop, label_text):
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(10)

        # Create a QCheckBox
        cb = QtWidgets.QCheckBox('')
        b = self.checkboxes.get(cb)
        if b:
            print ("THING: {0}".format(b))
        if isinstance(start, int):
            self.checkboxes[cb] = {}
            self.checkboxes[cb]['name'] = name
            self.checkboxes[cb]['start'] = start
            self.checkboxes[cb]['stop']  = stop

        cb.stateChanged.connect(self.onCheckboxChange)

        cb.setFont(self.smol_font)
        row.addWidget(cb)
        
        # Create a QLabel with left alignment
        label = QtWidgets.QLabel(label_text)
        label.setFont(self.smol_font)
        label.setAlignment(QtCore.Qt.AlignRight)  # Set left alignment
        row.setAlignment(QtCore.Qt.AlignLeft)
        row.addWidget(label)

        layout.addLayout(row)

    def showDialog(self):
        # Create and show the dialog when the button is clicked
        dialog = noSerialDialog()
        dialog.exec_()

    def onCheckboxChange(self):
        if not self.port.isOpen():
            self.showDialog()
            return()

        cb = self.sender()

        # need to know if a user clicked on a box or the program did.
        if self.programmatic_change: # the program changed it, so bail out
            self.programmatic_change = False
            return()

        self.programmatic_change = False

        # the user changed the check box, so do things...
        name  = self.checkboxes[cb]['name']
        start = self.checkboxes[cb]['start']
        stop  = self.checkboxes[cb]['stop']

        if cb.isChecked():
            if isinstance(start, int):
                text = "set {0} {1}".format(name, start)
            if isinstance(start, str):
                text = start
            text = text + '\r\n'
            self.port.write( text.encode() )
        else:
            if stop is not None: # sometimes we dont send a stop command
                if isinstance(stop, int):
                    text = "set {0} {1}".format(name, stop)
                if isinstance(stop, str):
                    text = stop
                text = text + '\r\n'
                self.port.write( text.encode() )


    # note that the state of the checkboxes only change when
    #  the program gets something from the serial. When a string comes in, it's parsed, then
    #  updateValues gets called. Notice how this changes the checkboxes programmatically
    #  and onCheckboxChange() will behave differently
    def updateValues(self, struct):
        for cb in self.checkboxes:
            n = self.checkboxes[cb].get('name')
            s = self.checkboxes[cb].get('start')
            t = struct.get(n)
            if n and t and s is not None:
                v = struct[n].get('value')
                if v:
                    v = float(v)
                    s = float(s)
                    self.programmatic_change = True
                    if v == s:
                        cb.setChecked(True)
                    else:
                        cb.setChecked(False)

        self.programmatic_change = False

        for e in self.entryboxes:
            n = self.entryboxes.get(e)
            t = struct.get(n)
            if n and t:
                v = struct[n].get('value')
                if v:
                    e.setText(v)

    def uartreqBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setStyleSheet("QGroupBox { border: 1px solid white; }")

        layout = QtWidgets.QVBoxLayout()

        combined_layout = QtWidgets.QHBoxLayout()
        combined_layout.setSpacing(0)

        # Create the first QVBoxLayout for radio buttons
        layout1 = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('uart_req test')
        label.setFont(self.big_font)
        layout1.addWidget(label)

        self.checkBoxRow(layout1, 'curr_max', 40,
                         None, 'set curr_max 40')
        self.checkBoxRow(layout1, 'motor_sensor', 0,
                         None, 'set motor_sensor 0 (0 = SL, "sensorless")')
        self.checkBoxRow(layout1, 'input_opt', 8, 1,
                         'set input_opt 8 (8, input from UART)')
        self.checkBoxRow(layout1, 'uart_req', 3, 0,
                         'set uart_req (ranges from 0 to 6)')

        # Create the second QVBoxLayout
        layout2 = QtWidgets.QVBoxLayout()
        # stays empty for nowx

        combined_layout.addLayout(layout1)
        combined_layout.addLayout(layout2)

        layout.addLayout(combined_layout)

        label = QtWidgets.QLabel("uart_req spins at fixed levels ranging from 0 (nothing) to 6.  click = 3,  unclick = 0.  Caution: this can really crank up the speed of the motor")

        label.setFont(self.smol_font)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        layout.addWidget(label)
        box.setLayout(layout)

        return box

    def openLoopBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setStyleSheet("QGroupBox { border: 1px solid white; }")

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

        self.checkBoxRow(layout1, 'curr_max', 40, None, 'set curr_max 40 (40 Amps, something safe)')
        self.checkBoxRow(layout1, 'input_opt', 8, 1, 'set input_opt 8 (8 = UART,  meaning: receive control input from UART)')
        self.checkBoxRow(layout1, 'motor_sensor', 2, None, 'set motor_sensor 2 (2 = open loop)')
        self.checkBoxRow(layout1, 'ol_step', 20, None, 'set ol_step 20 (number of steps per pulse)')
        self.checkBoxRow(layout1, 'uart_req', 10, 0, 'set uart_req 10 (requesting 10 Amps,  uncheck to stop)')

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

        label = QtWidgets.QLabel("Selecting these click boxes should get your motor spinning.  To stop,  unselect the last checkbox.  If the motor is attempting to spin or not spinning check your wiring and controller.  If it's a large motor you may need to set curr_max to something > 40 Amps.  If you stream data by selecting the \"Data\" button below you should see that 10 phase Amps are being used.")
        label.setFont(self.smol_font)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        layout.addWidget(label)
        box.setLayout(layout)

        return box

    def throttleBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setStyleSheet("QGroupBox { border: 1px solid white; }")

        layout = QtWidgets.QVBoxLayout()

        combined_layout = QtWidgets.QHBoxLayout()
        combined_layout.setSpacing(0)

        # Create the first QVBoxLayout for radio buttons
        layout1 = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Throttle test')
        label.setFont(self.big_font)
        layout1.addWidget(label)

        self.checkBoxRow(layout1, 'curr_max', 40,
                         None, 'set curr_max 40 (40 Amps, something safe)')
        self.checkBoxRow(layout1, 'motor_sensor', 0,
                         None, 'set motor_sensor 0 (0 = SL, "sensorless")')
        self.checkBoxRow(layout1, 'input_opt', 1, 0,
                         'set input_opt 1 (checked sets to 1 = ADC1, unchecked sets 8 = UART )')
        self.setValueRow(layout1, 'adc1_min', 'set adc1_min', 'set minimum value for adc1 range')
        self.setValueRow(layout1, 'adc1_max', 'set adc1_max', 'set maximum value for adc1 range')

        # Create the second QVBoxLayout
        layout2 = QtWidgets.QVBoxLayout()
        # stays empty for nowx

        combined_layout.addLayout(layout1)
        combined_layout.addLayout(layout2)

        layout.addLayout(combined_layout)

        label = QtWidgets.QLabel("Physically connect a potentiometer to the adc1 input of your mesc board.  Select sensorless mode, and change the set input_opt value to 1 to send adc1 values to your controller.  If you stream data by selecting the \"Data\" button below you should see the throttle widget update when you turn your potentiometer.")

        label.setFont(self.smol_font)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        layout.addWidget(label)
        box.setLayout(layout)

        return box

    def titleBox(self):
        box = QtWidgets.QGroupBox('')
        box.setFont(self.big_font)
        box.setFixedHeight(220) # I dislike this is the only way to control space around text
        if self.os == 'Win':
            box.setFixedHeight(500) # difference in size is very weird 
            
        box.setStyleSheet("QGroupBox { border: 3px solid white; }")
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

        
class noSerialDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        label = QLabel('Serial port must be open to use this page.', self)
        close_button = QtWidgets.QPushButton('Okay', self)
        close_button.clicked.connect(self.close)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(close_button)
        self.setLayout(vbox)
        self.setWindowTitle('Dialog Box')
        self.setGeometry(180, 300, 180, 150)
