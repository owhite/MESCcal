#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget
from PyQt5.QtCore import Qt

class CustomScrollArea(QScrollArea):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            print("Left arrow key pressed in CustomScrollArea")
            # Handle left arrow key press here
        elif event.key() == Qt.Key_Right:
            print("Right arrow key pressed in CustomScrollArea")
            # Handle right arrow key press here
        else:
            # Call the base class implementation for other key events
            super().keyPressEvent(event)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        scroll_area = CustomScrollArea(self)
        widget = QWidget(self)
        scroll_area.setWidget(widget)
        self.setCentralWidget(scroll_area)

    # Other methods and UI setup can be added here

if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
