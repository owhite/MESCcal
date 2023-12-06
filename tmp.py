#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton


class LabelApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Create two buttons
        self.create_button = QPushButton('Create Labels', self)
        self.create_button.clicked.connect(self.create_labels)
        self.layout.addWidget(self.create_button)

        self.delete_button = QPushButton('Delete Labels', self)
        self.delete_button.clicked.connect(self.delete_labels)
        self.layout.addWidget(self.delete_button)

        # Create an empty list to store labels
        self.labels = []

    def create_labels(self):
        # Create three labels and add them to the layout and the list
        for i in range(3):
            label = QLabel(f'Label {i+1}', self)
            self.layout.addWidget(label)
            self.labels.append(label)

    def delete_labels(self):
        # Delete each label from the layout and remove it from the list
        for label in self.labels:
            label.deleteLater()
        self.labels = []


def run_app():
    app = QApplication(sys.argv)
    label_app = LabelApp()
    label_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
