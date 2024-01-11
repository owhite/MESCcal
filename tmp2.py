#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolButton, QMenu, QAction, QHBoxLayout
from PyQt5.QtCore import Qt, QEvent

class ToolButtonExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        tool_button1 = QToolButton()
        tool_button1.setText("ToolButton 1")
        tool_button1.clicked.connect(self.showMenu)
        tool_button1.mousePressEvent = self.toolButtonMousePressEvent  # Override mousePressEvent
        layout.addWidget(tool_button1)

        tool_button2 = QToolButton()
        tool_button2.setText("ToolButton 2")
        tool_button2.clicked.connect(self.showMenu)
        tool_button2.mousePressEvent = self.toolButtonMousePressEvent  # Override mousePressEvent
        layout.addWidget(tool_button2)

        self.setLayout(layout)

        self.setWindowTitle('QToolButton Example')
        self.setGeometry(300, 300, 300, 100)

    def showMenu(self):
        sender_button = self.sender()
        if sender_button:
            menu = QMenu(self)
            menu.addAction(QAction("Action 1", self))
            menu.addAction(QAction("Action 2", self))
            menu.addAction(QAction("Action 3", self))

            action = menu.exec_(sender_button.mapToGlobal(sender_button.rect().bottomLeft()))
            if action:
                print(f"Selected action: {action.text()}")

    def toolButtonMousePressEvent(self, event):
        print("QToolButton clicked by mouse")

        super().mousePressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            print(f'Key pressed: {key}')
            return True  # Consume the event

        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = ToolButtonExample()
    example.installEventFilter(example)
    example.show()
    sys.exit(app.exec_())
