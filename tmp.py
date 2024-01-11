#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent, QPoint, QTimer
from PyQt5.QtGui import QMouseEvent
from functools import partial

class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 100)
        self.layout = QHBoxLayout(self)
        label = QLabel('QToolButton Popup')

        self.tools = []
        self.tool_index = 0
        self.toolButtonHighlightIndex = 0
        self.toolButtonButtons = {}

        tool = self.createTool("B1", "thing1")
        self.layout.addWidget(tool)
        self.tools.append(tool)
        self.tool_index = self.tool_index + 1

        tool = self.createTool("B2", "thing2")
        self.layout.addWidget(tool)
        self.tools.append(tool)
        self.tool_index = self.tool_index + 1
        
        self.layout.addWidget(label)

    def navigateTools(self, direction):
        self.tool_index = (self.tool_index + direction) % len(self.tools)

        print(self.tool_index)
        count = 0
        for t in self.tools:
            if count == self.tool_index:
                t.setStyleSheet("background-color: yellow")
                t.menu().setStyleSheet("background-color: red")
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
            print("OPEN")
            self.openTool()

        # Highlight the QToolButton in the current row using up/down arrows
        elif key == Qt.Key_Up:
            print("UP")
        elif key == Qt.Key_Down:
            print("DOWN")

    def openTool(self):
        print("show")
        self.toolButtonHighlightIndex = 0
        t = self.tools[self.tool_index]
        t.menu().setStyleSheet("")
        self.toolButtonHightlight(t)
        t.showMenu()

    def createTool(self, button_text, layout_label):
        tool = QToolButton() # confusing because this code calls this a "tool", but ¯\_(ツ)_/
        tool.setText(button_text)
        tool.setPopupMode(QToolButton.InstantPopup)

        widget = QWidget()
        widget_layout = QGridLayout(widget)
        widget_label = QLabel(layout_label)

        # Adjust spacing between buttons
        widget_layout.setHorizontalSpacing(4)
        widget_layout.setVerticalSpacing(4)

        widget.setStyleSheet("background-color: white;" "border :1px solid black;")

        buttons = []
        for i in range(3):
            for j in range(3):
                num = i * 3 + j + 1
                button = QPushButton(f' {num} ')
                buttons.append(button)
                button.setStyleSheet("background-color: white;" "border :1px solid black;")
                button.clicked.connect(partial(self.onToolButtonClick, num, widget_label))
                widget_layout.addWidget(button, i+1, j+1)

        widget_layout.addWidget(widget_label, 0, 0, 1, 3)

        widget_action = QWidgetAction(tool)
        widget_action.setDefaultWidget(widget)

        widget_menu = QMenu(tool)
        self.toolButtonButtons[tool] = buttons

        widget_menu.addAction(widget_action)
        widget_menu.installEventFilter(self)

        tool.setMenu(widget_menu)

        return tool

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            print(f'Key pressed in submenu: {key} :: {obj}')

            if key == Qt.Key_Up:
                print("UP")
            elif key == Qt.Key_Down:
                print("DOWN")
            elif key == Qt.Key_Left:
                print("LEFT")
            elif key == Qt.Key_Right:
                print("RIGHT")
            elif key == Qt.Key_Enter or key == Qt.Key_Return:
                print("TOOL ENTER")
                obj.showMenu()
                

        return super().eventFilter(obj, event)

    def toolButtonHightlight(self, obj):
        print(obj)
        b = self.toolButtonButtons[obj][self.toolButtonHighlightIndex]
        b.setStyleSheet("background-color: grey;" "border :1px solid black;")

    def onToolButtonClick(self, key, label):
        print(f"widget_button clicked! {key} :: {label.text()}")
        if type(key) is int:
            label.setText(label.text() + str(key))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()
    sys.exit(app.exec_())
