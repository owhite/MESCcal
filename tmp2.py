#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
from configparser import ConfigParser

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Config Window")

        # UI components
        self.label = QLabel("Enter a value:")
        self.line_edit = QLineEdit()
        self.save_button = QPushButton("Save Config")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect signals
        self.save_button.clicked.connect(self.save_config)

    def save_config(self):
        config = ConfigParser()

        # Example configuration
        config['Settings'] = {
            'value': self.line_edit.text()
        }

        # Save to a file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("Config saved!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())
