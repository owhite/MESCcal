#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent, QPoint, QTimer
from PyQt5.QtGui import QMouseEvent
from functools import partial

class Test(QWidget):
    def __init__(self):
        super().__init__()

        # Set the initial position of the window
        self.move(100, 100)  # Set x=100, y=100

        self.resize(200, 100)
        self.layout = QHBoxLayout(self)

        self.tools = []
        self.tool_index = 0
        self.toolButtonHighlightIndex = 0
        self.toolButtonButtons = {}

        tool = self.createTool("req_adc1", "12")
        self.layout.addWidget(tool)
        self.tools.append(tool)
        tool.clicked.connect(self.openTool)
        tool.mousePressEvent = self.toolButtonMousePressEvent 

        # self.tool_index = self.tool_index + 1

        tool = self.createTool("curr_max", "40.0")
        self.layout.addWidget(tool)
        self.tools.append(tool)
        tool.clicked.connect(self.openTool)
        tool.mousePressEvent = self.toolButtonMousePressEvent 

        # self.tool_index = self.tool_index + 1
        self.navigateTools(0)
        
    def toolButtonMousePressEvent(self, event):
        sender_button = self.sender()
        print(f"QToolButton clicked by mouse {self}")

    def onToolButtonClick2(self):
        sender_button = self.sender()
        if sender_button:
            print(f"Opened: {sender_button.text()}")

    def navigateTools(self, direction):
        self.tool_index = (self.tool_index + direction) % len(self.tools)

        count = 0
        for t in self.tools:
            if count == self.tool_index:
                t.setStyleSheet("background-color: white")
                t.menu().setStyleSheet("background-color: white")
            else:
                t.setStyleSheet("")
                t.menu().setStyleSheet("")
            count = count + 1

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            self.navigateTools(-1)
        elif key == Qt.Key_Right:
            self.navigateTools(1)

        # Show the layout when pressing the Enter key
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.openTool()

        # Highlight the QToolButton in the current row using up/down arrows
        elif key == Qt.Key_Up:
            print("UP")
        elif key == Qt.Key_Down:
            print("DOWN")

    def openTool(self):
        print("HERE")
        t = self.tools[self.tool_index]
        t.setStyleSheet("background-color: white")
        t.menu().setStyleSheet("background-color: white")
        self.toolButtonHighlightIndex = 0
        self.toolButtonHighlight(t.menu())
        t.showMenu()

    def createTool(self, button_text, layout_label):
        tool = QToolButton() # confusing because this code calls this a "tool", but ¯\_(ツ)_/

        tool.setText(button_text + '\n' + layout_label)
        tool.setPopupMode(QToolButton.InstantPopup)

        widget = QWidget()
        widget.setStyleSheet("background-color: white;" "border :1px solid black;")
        widget_menu = QMenu(tool)
        widget_layout = QGridLayout(widget)
        widget_label = QLabel(layout_label)
        widget_layout.addWidget(widget_label, 0, 0, 1, 4)

        # Adjust spacing between buttons
        widget_layout.setHorizontalSpacing(4)
        widget_layout.setVerticalSpacing(4)

        buttons = []
        keys = [
            '7', '8', '9', '<<',
            '4', '5', '6', 'cancel',
            '1', '2', '3', '',
            '0', '.', 'enter', ''
        ]

        row = 1
        col = 0

        for key in keys:
            button = QPushButton(key, self)
            button.clicked.connect(partial(self.onToolButtonClick, key, button_text, widget_label))
            buttons.append(button)
            if key == '':
                button.hide()
            elif key == 'enter':
                widget_layout.addWidget(button, row, col, 1, 2)
            else:
                widget_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        widget_action = QWidgetAction(tool)
        widget_action.setDefaultWidget(widget)

        self.toolButtonButtons[widget_menu] = buttons

        widget_menu.addAction(widget_action)
        widget_menu.installEventFilter(self)

        tool.setMenu(widget_menu)

        return tool

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_Up:
                if self.toolButtonHighlightIndex == 3:
                    self.toolButtonHighlightIndex = 14
                elif self.toolButtonHighlightIndex == 7:
                    self.toolButtonHighlightIndex = 3
                elif self.toolButtonHighlightIndex == 14:
                    self.toolButtonHighlightIndex = 7
                else:
                    self.toolButtonHighlightIndex = (self.toolButtonHighlightIndex - 4) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Down:
                if self.toolButtonHighlightIndex == 7:
                    self.toolButtonHighlightIndex = 14
                elif self.toolButtonHighlightIndex == 14:
                    self.toolButtonHighlightIndex = 3
                else:
                    self.toolButtonHighlightIndex = (self.toolButtonHighlightIndex + 4) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Left:
                self.toolButtonHighlightIndex = (self.toolButtonHighlightIndex - 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Right:
                self.toolButtonHighlightIndex = (self.toolButtonHighlightIndex + 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Enter or key == Qt.Key_Return:
                b = self.toolButtonButtons[obj][self.toolButtonHighlightIndex]
                b.click()
                return True

        return super().eventFilter(obj, event)

    def toolButtonHighlight(self, obj):
        for n, b in enumerate(self.toolButtonButtons[obj]):
            if n == self.toolButtonHighlightIndex:
                b.setStyleSheet("background-color: grey;" "border :1px solid black;")
            else:
                b.setStyleSheet("background-color: white;" "border :1px solid black;")

    def onToolButtonClick(self, key, value, label):
        button = self.sender() 
        if button: # a lot of ifs!
            action = button.parentWidget()
            if action:
                menu = action.parentWidget()
                if menu:
                    tool = menu.parentWidget()
        try:
            int_value = int(key)
            label.setText(label.text() + str(int_value))
            print(label.text())
        except:
            if (key) == 'cancel':
                menu.hide()
            if (key) == '<<':
                s = label.text()
                label.setText(s[:-1])
            if (key) == '.':
                label.setText(label.text() + key)
            if (key) == 'enter':
                tool.setText(value + '\n' + label.text())
                print(f"set {value} {label.text()}")
                menu.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()
    sys.exit(app.exec_())
