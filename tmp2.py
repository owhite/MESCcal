#!/usr/bin/env python3

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


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QVBoxLayout, QLabel, QWidget, QMenu, QWidgetAction
from PyQt5.QtCore import Qt, QEvent, QTimer, QPoint

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.current_tool_button = None  # Track the currently focused QToolButton

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create QToolButtons
        self.tool_buttons = [self.createToolButton(f'ToolButton {i + 1}') for i in range(2)]
        for tool_button in self.tool_buttons:
            layout.addWidget(tool_button)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QToolButton Navigation Example')
        self.show()

    def createToolButton(self, label):
        tool_button = QToolButton()
        tool_button.setText(label)
        tool_button.setPopupMode(QToolButton.InstantPopup)

        widget = QWidget()
        widget_layout = QVBoxLayout(widget)
        widget_label = QLabel(f'Additional Label for {label}')

        # Add space between widgets
        widget_layout.addSpacing(10)

        # Create a grid of buttons (just for demonstration)
        for i in range(3):
            for j in range(3):
                button = QToolButton()
                button.setText(f'{i * 3 + j + 1}')
                widget_layout.addWidget(button)

        widget_layout.addWidget(widget_label)

        widget_action = QWidgetAction(tool_button)
        widget_action.setDefaultWidget(widget)

        widget_menu = QMenu(tool_button)
        widget_menu.addAction(widget_action)
        tool_button.setMenu(widget_menu)

        tool_button.installEventFilter(self)  # Install event filter for QToolButton

        return tool_button

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn and obj in self.tool_buttons:
            self.current_tool_button = obj
            self.current_tool_button.setStyleSheet("background-color: yellow")
            return True
        return False

    def keyPressEvent(self, event):
        key = event.key()

        # Navigate between QToolButtons using left/right arrows
        if key == Qt.Key_Left:
            self.tool_buttons[0].setStyleSheet("background-color: yellow")
            self.tool_buttons[1].setStyleSheet("")
            self.navigate(-1)
        elif key == Qt.Key_Right:
            self.tool_buttons[0].setStyleSheet("")
            self.tool_buttons[1].setStyleSheet("background-color: yellow")
            self.navigate(1)

        # Show the layout when pressing the Enter key
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            print("OPEN")
            self.showLayout()

    def navigate(self, direction):
        if self.current_tool_button in self.tool_buttons:
            current_index = self.tool_buttons.index(self.current_tool_button)
            new_index = (current_index + direction) % len(self.tool_buttons)

            # Remove highlight from the current tool button
            self.current_tool_button.setStyleSheet("")

            # Set focus on the new tool button
            self.tool_buttons[new_index].setFocus()

            # Highlight the new tool button (for demonstration purposes)
            self.tool_buttons[new_index].setStyleSheet("background-color: yellow")

    def showLayout(self):
        print("show")
        if self.current_tool_button:
            print("show2")
            # Simulate a mouse press event to open the menu and show the layout
            point = self.current_tool_button.rect().center()
            global_point = self.current_tool_button.mapToGlobal(point)
            mouse_event = QEvent(QEvent.MouseButtonPress)
            mouse_event.setPos(QPoint(global_point.x(), global_point.y()))
            QApplication.postEvent(self.current_tool_button, mouse_event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
