#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        button1 = QPushButton('Button 1', self)
        button2 = QPushButton('Button 2', self)

        button1.clicked.connect(self.on_button_click)
        button2.clicked.connect(self.on_button_click)

        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)

    def on_button_click(self):
        sender_button = self.sender()  # Get the button that emitted the signal
        if sender_button:
            x, y = sender_button.pos().x(), sender_button.pos().y()
            print(f'Button "{sender_button.text()}" clicked at position ({x}, {y}).')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())


