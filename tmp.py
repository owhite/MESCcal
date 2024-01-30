#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class KeyPressWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a QLabel to display key presses
        self.label = QLabel('Press a key...')
        
        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Set up the window
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Key Presses')

    def keyPressEvent(self, event):
        # Handle key presses and display key code in hexadecimal
        key = event.key()
        text = f'Key Pressed: {hex(key)}'
        self.label.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KeyPressWidget()
    window.show()
    sys.exit(app.exec_())
