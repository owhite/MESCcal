#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent, QPoint, QTimer
from PyQt5.QtGui import QMouseEvent

class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 100)
        self.layout = QHBoxLayout(self)
        label = QLabel('QToolButton Popup')

        self.tool_buttons = []
        self.tool_index = 0
        tool_button = self.createToolButton("B1", "thing1")
        self.layout.addWidget(tool_button)
        self.tool_buttons.append(tool_button)
        self.tool_index = self.tool_index + 1

        tool_button = self.createToolButton("B2", "thing2")
        self.layout.addWidget(tool_button)
        self.tool_buttons.append(tool_button)
        self.tool_index = self.tool_index + 1
        
        self.layout.addWidget(label)

    def keyPressEvent(self, event):
        key = event.key()

        # Navigate between QToolButtons using left/right arrows
        if key == Qt.Key_Left:
            self.navigate(-1)
        elif key == Qt.Key_Right:
            self.navigate(1)

        # Show the layout when pressing the Enter key
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            print("OPEN")
            self.showLayout()

        # Highlight the QToolButton in the current row using up/down arrows
        elif key == Qt.Key_Up:
            self.highlight(-1)
        elif key == Qt.Key_Down:
            self.highlight(1)

    def showLayout(self):
        print("show")
        t = self.tool_buttons[self.tool_index]
        t.menu().setStyleSheet("")
        t.showMenu()

    def showLayout2(self):
        print("show")
        t = self.tool_buttons[self.tool_index]
        # Simulate a mouse press event to open the menu and show the layout
        point = t.rect().center()
        global_point = t.mapToGlobal(point)
        mouse_event = QMouseEvent(
            QEvent.MouseButtonPress,
            global_point,
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier,
        )
        QApplication.postEvent(t, mouse_event)

    def navigate(self, direction):
        self.tool_index = (self.tool_index + direction) % len(self.tool_buttons)

        print(self.tool_index)
        count = 0
        for t in self.tool_buttons:
            if count == self.tool_index:
                t.setStyleSheet("background-color: yellow")
                t.menu().setStyleSheet("background-color: red")
            else:
                t.setStyleSheet("")
                t.menu().setStyleSheet("")
            count = count + 1


    def highlight(self, direction):
        current_index = self.tool_buttons.index(self.focusWidget())
        row, col = self.layout.getItemPosition(self.tool_buttons[current_index])

        new_row = row + direction
        if 0 <= new_row < self.layout.rowCount():
            tool_button_in_row = self.layout.itemAtPosition(new_row, col).widget()

    def createToolButton(self, button_text, layout_label):
        tool_button = QToolButton()
        tool_button.setText(button_text)
        tool_button.setPopupMode(QToolButton.InstantPopup)

        widget = QWidget()
        widget_layout = QGridLayout(widget)
        widget_label = QLabel(layout_label)

        # Adjust spacing between buttons
        widget_layout.setHorizontalSpacing(2)
        widget_layout.setVerticalSpacing(2)

        # Create a grid of buttons
        for i in range(3):
            for j in range(3):
                button = QPushButton(f'{i * 3 + j + 1}')
                button.setStyleSheet("background-color: red")
                button.clicked.connect(self.onWidgetButtonClick)
                widget_layout.addWidget(button, i+1, j+1)

        widget_layout.addWidget(widget_label, 0, 0, 1, 3)

        widget_action = QWidgetAction(tool_button)
        widget_action.setDefaultWidget(widget)

        widget_menu = QMenu(tool_button)
        widget_menu.addAction(widget_action)

        # Install event filter for the submenu (widget_menu)
        widget_menu.installEventFilter(self)

        tool_button.setMenu(widget_menu)

        return tool_button

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()

            # Handle key events within the submenu here
            print(f'Key pressed in submenu: {key}')

        return super().eventFilter(obj, event)

    def createToolButton2(self, button_text, layout_label):
        tool_button = QToolButton()
        tool_button.setText(button_text)
        tool_button.setPopupMode(QToolButton.InstantPopup)

        widget = QWidget()
        widget_layout = QGridLayout(widget)
        widget_label = QLabel(layout_label)

        # Adjust spacing between buttons
        widget_layout.setHorizontalSpacing(2)
        widget_layout.setVerticalSpacing(2)

        # Create a grid of buttons
        for i in range(3):
            for j in range(3):
                button = QPushButton(f'{i * 3 + j + 1}')
                button.setStyleSheet("background-color: red")
                button.clicked.connect(self.onWidgetButtonClick)
                widget_layout.addWidget(button, i+1, j+1)

        widget_layout.addWidget(widget_label, 0, 0, 1, 3)

        widget_action = QWidgetAction(tool_button)
        widget_action.setDefaultWidget(widget)

        widget_menu = QMenu(tool_button)
        widget_menu.addAction(widget_action)
        tool_button.setMenu(widget_menu)

        return tool_button

    def onWidgetButtonClick(self):
        print("widget_button clicked!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()
    sys.exit(app.exec_())
