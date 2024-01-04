#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QCheckBox, QLineEdit
import Events
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Highlightable Widgets Example')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        widget_list = []
        self.line_edit = QLineEdit(self)
        self.highlightable_line_edit = Events.HLLineEdit(self.line_edit, widget_list)
        self.highlightable_line_edit.lineEditFocused.connect(self.handleLineEditFocus)

        self.button1 = QPushButton('Button 1')
        self.button2 = QPushButton('Button 2')
        self.button3 = QPushButton('Button 3')

        self.highlightable_button1 = Events.HLButton(self.button1)
        self.highlightable_button2 = Events.HLButton(self.button2)
        self.highlightable_button3 = Events.HLButton(self.button3)

        self.highlightable_button1.buttonPressed.connect(self.handleButtonPress)  
        self.highlightable_button2.buttonPressed.connect(self.handleButtonPress)  
        self.highlightable_button3.buttonPressed.connect(self.handleButtonPress)  

        self.checkBox1 = QCheckBox('CheckBox 1')
        self.checkBox2 = QCheckBox('CheckBox 2')
        self.checkBox3 = QCheckBox('CheckBox 3')

        self.highlightable_checkBox1 = Events.HLCheckBox(self.checkBox1)
        self.highlightable_checkBox2 = Events.HLCheckBox(self.checkBox2)
        self.highlightable_checkBox3 = Events.HLCheckBox(self.checkBox3)

        self.highlightable_checkBox1.checkBoxStateChanged.connect(self.handleCheckBoxStateChange)
        self.highlightable_checkBox2.checkBoxStateChanged.connect(self.handleCheckBoxStateChange)
        self.highlightable_checkBox3.checkBoxStateChanged.connect(self.handleCheckBoxStateChange)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.button1)
        layout.addWidget(self.checkBox1)
        layout.addWidget(self.button2)
        layout.addWidget(self.checkBox2)
        layout.addWidget(self.button3)
        layout.addWidget(self.checkBox3)

        widget_list.append(self.line_edit)
        widget_list.append(self.button1)
        widget_list.append(self.checkBox1)
        widget_list.append(self.button2)
        widget_list.append(self.checkBox2)
        widget_list.append(self.button3)
        widget_list.append(self.checkBox3)

    def handleButtonPress(self):
        print('Button Pressed!')

    def handleCheckBoxStateChange(self, isChecked):
        print(f'CheckBox State Changed: {isChecked}')

    def handleLineEditFocus(self):
        print('QLineEdit Focused!')

    def keyPressEvent(self, event):
        if event.text() == 'g':
            print("get")
        if event.key() == Qt.Key_Return:
            self.button1.click()
        elif event.key() == Qt.Key_Left:
            self.setFocusToPreviousWidget()
        elif event.key() == Qt.Key_Right:
            self.setFocusToNextWidget()

    def setFocusToPreviousWidget(self):
        current_widget = self.focusWidget()
        if current_widget:
            next_widget = current_widget.focusPreviousChild()
            if not next_widget:
                next_widget = self.highlightable_line_edit.lineEdit
            next_widget.setFocus()

    def setFocusToNextWidget(self):
        current_widget = self.focusWidget()
        if current_widget:
            next_widget = current_widget.focusNextChild()
            if not next_widget:
                next_widget = self.button1  # Set it to the first widget if at the end
            next_widget.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = MainWindow()
    example.show()
    sys.exit(app.exec_())
