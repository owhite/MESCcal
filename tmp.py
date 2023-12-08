#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # List to hold references to push buttons
        self.buttons = []

        # Create push buttons using a for loop
        for i in range(1, 5):
            push_button = QPushButton(f'Button {i}')
            push_button.setCheckable(True)
            self.buttons.append(push_button)
            vbox.addWidget(push_button)

        # Connect the clicked signal to a slot function
        for button in self.buttons:
            button.clicked.connect(self.on_button_clicked)

        self.setWindowTitle('QPushButton Example')
        self.show()

    def on_button_clicked(self):
        # Slot function to handle button clicks
        sender_button = self.sender()
        print(f'Clicked button: {sender_button.text()}, Checked: {sender_button.isChecked()}')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
