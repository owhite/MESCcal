#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class LabelApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Label Example')

        self.layout = QVBoxLayout(self)

        self.create_label_button = QPushButton('Create Label', self)
        self.create_label_button.clicked.connect(self.create_label)

        self.remove_label_button = QPushButton('Remove Label', self)
        self.remove_label_button.clicked.connect(self.remove_label)

        self.layout.addWidget(self.create_label_button)
        self.layout.addWidget(self.remove_label_button)

        self.label = None  # Initialize label as None

        self.show()

    def create_label(self):
        if self.label is None:
            self.label = QLabel('Hello, I am a label!', self)
            self.layout.addWidget(self.label)

    def remove_label(self):
        if self.label is not None:
            self.layout.removeWidget(self.label)
            self.label.deleteLater()  # Delete the label widget
            self.label = None  # Set label to None to recreate it if needed

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LabelApp()
    sys.exit(app.exec_())
