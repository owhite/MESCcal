#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QLabel
from PyQt5.QtGui import QFont  # Import QFont from QtGui

class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.big_font = QFont()
        self.big_font.setPointSize(18)  # Change the font size as needed
        self.font = QFont()
        self.font.setPointSize(12)  # Change the font size as needed

        layout.addWidget(self.openLoopBox())

        # Set the main layout for the main window
        self.setLayout(layout)

    def openLoopBox(self):
        box = QGroupBox('')
        box.setFont(self.big_font)

        combined_layout = QHBoxLayout()

        # Create the first QVBoxLayout for radio buttons
        layout1 = QVBoxLayout()

        label = QLabel('Run in open loop') 
        label.setFont(self.big_font)
        layout1.addWidget(label)

        label = QLabel("Running in open loop mode turns the motor with no feedback control.")
        label.setFont(self.font)
        layout1.addWidget(label)
        self.createRow(layout1, "set curr_max 40", "set curr_max 40 (something safe)")
        self.createRow(layout1, "set SL_sensor OL", "set SL_sensor OL \"open loop\"")
        self.createRow(layout1, "set input_opt 8", "set input_opt 8 (sends data to UART)")
        self.createRow(layout1, "set ol_step 20", "set ol_step 20 (number of steps per pulse)")

        # Create the second QVBoxLayout
        layout2 = QVBoxLayout()
        row = QHBoxLayout()
        label = QLabel("row2")
        label.setFont(self.font)
        row.addWidget(label)
        layout2.addLayout(row)

        combined_layout.addLayout(layout1)
        combined_layout.addLayout(layout2)
        box.setLayout(combined_layout)

        return(box)

    def createRow(self, layout, n, text):
        row = QHBoxLayout()
        cb = QCheckBox(text)
        cb.stateChanged.connect(lambda state: self.on_checkbox_change(n, state))
        cb.setFont(self.font)
        row.addWidget(cb)
        layout.addLayout(row)

    def on_checkbox_change(self, checkbox_name, state):
        if state == 2:  # Checked state
            print(f'{checkbox_name} is enabled')
        else:  # Unchecked state
            print(f'{checkbox_name} is disabled')


if __name__ == '__main__':
    app = QApplication([])
    window = ExampleWidget()
    window.show()
    app.exec_()
