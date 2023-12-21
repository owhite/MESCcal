#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QRadioButton, QLabel
from PyQt5.QtGui import QFont  # Import QFont from QtGui

class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create the first group box
        group_box1 = QGroupBox('Group Box 1')

        # Set a larger font size for the text in 'Group Box 1'
        font = QFont()
        font.setPointSize(10)  # Change the font size as needed
        group_box1.setFont(font)

        # Create the QVBoxLayout to contain radio buttons and labels
        combined_layout = QVBoxLayout()

        # Create the first QVBoxLayout for radio buttons
        layout1 = QVBoxLayout()
        for i in range(5):
            radio_button = QRadioButton(f'Radio {i+1}')
            layout1.addWidget(radio_button)

        # Create the second QVBoxLayout for labels
        layout2 = QVBoxLayout()
        for i in range(5):
            label = QLabel(f'Label {i+1}')
            layout2.addWidget(label)

        # Add layout1 and layout2 to the combined layout
        combined_layout.addLayout(layout1)
        combined_layout.addLayout(layout2)

        # Set the combined layout as the layout for group_box1
        group_box1.setLayout(combined_layout)

        # Add group_box1 to the main layout
        layout.addWidget(group_box1)

        # Set the main layout for the main window
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    window = ExampleWidget()
    window.show()
    app.exec_()
