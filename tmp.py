#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt

class HighlightableComboBox(QComboBox):
    def __init__(self, items, parent=None):
        super(HighlightableComboBox, self).__init__(parent)
        self.addItems(items)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet("QComboBox:focus { background-color: yellow; }")

    def navigate(self, direction):
        print("NEVER")
        self.comboboxes[self.currentIndex].setStyleSheet("background-color: yellow;" if highlighted else "")
        self.currentIndex = (self.currentIndex + direction) % len(self.comboboxes)
        self.setHighlight(True)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Arrow Key Navigation Example')
        layout = QVBoxLayout(self)

        self.combobox1 = HighlightableComboBox(['Item 1', 'Item 2', 'Item 3'])
        self.combobox2 = HighlightableComboBox(['A', 'B', 'C'])
        self.combobox3 = HighlightableComboBox(['Option X', 'Option Y', 'Option Z'])

        layout.addWidget(self.combobox1)
        layout.addWidget(self.combobox2)
        layout.addWidget(self.combobox3)


    def keyPressEvent(self, event):
        current_widget = self.focusWidget()

        if event.key() == Qt.Key_Left:
            print("LEFT")
            next_widget = current_widget.focusPreviousChild()
        elif event.key() == Qt.Key_Right:
            next_widget = current_widget.focusNextChild()
            print("RIGHT")
        elif event.key() == Qt.Key_Return:
            print("ACTIVATE")
        else:
            super(MainWindow, self).keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
