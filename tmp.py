#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtCore import Qt, QObject, pyqtSignal


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.buttons = []

        self.setWindowTitle('Arrow Key Navigation Example')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.button1 = QPushButton('Button 1')
        self.button2 = QPushButton('Button 2')
        self.button3 = QPushButton('Button 3')

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.button1.buttonPressed.connect(self.handleButtonPress)


        self.highlightable_button1 = HighlightableButton(self.button1)
        self.highlightable_button2 = HighlightableButton(self.button2)
        self.highlightable_button3 = HighlightableButton(self.button3)

        self.label = QLabel('Press a key...', self)
        layout.addWidget(self.label)

    def handleButtonPress(self):
        print("PRESS")

class HighlightableButton(QObject):
    highlighted = pyqtSignal(bool)

    def __init__(self, button):
        super(HighlightableButton, self).__init__()
        self.button = button
        self.button.setFocusPolicy(Qt.StrongFocus)
        self.button.setAutoDefault(True)
        self.button.installEventFilter(self)

    def eventFilter(self, obj, event):
        print(self.sender)
        if obj == self.button:
            print(event.type())
            if event.type() == event.FocusIn:
                self.highlighted.emit(True)
                self.button.setStyleSheet("background-color: yellow;")
            elif event.type() == event.FocusOut:
                self.highlighted.emit(False)
                self.button.setStyleSheet("")
            elif event.type() == event.KeyPress:
                key = event.key()
                print(key)
                # self.keyPressed.emit(key)  # Emit the key code signal

        return super(HighlightableButton, self).eventFilter(obj, event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
