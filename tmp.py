#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.checkbox = QCheckBox("Check me", self.central_widget)
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.checkbox)

        # Variable to track if the change is programmatic or user-initiated
        self.programmatic_change = False

        # Example of changing the checkbox state programmatically
        # Uncomment this line to see the programmatic change
        # self.checkbox.setChecked(True)

    def checkbox_state_changed(self, state):
        if not self.programmatic_change:
            if state == Qt.Checked:
                print("User checked the checkbox")
            else:
                print("User unchecked the checkbox")

        # Reset the programmatic_change flag
        self.programmatic_change = False

    def set_checkbox_programmatically(self, checked):
        # Set the programmatic_change flag to True before changing the checkbox state
        self.programmatic_change = True
        self.checkbox.setChecked(checked)

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.setGeometry(100, 100, 300, 200)
    window.show()
    app.exec_()
