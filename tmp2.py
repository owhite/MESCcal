#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTextEdit, QRadioButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set up the main window
        self.setWindowTitle('Tabs and QTextEdit Example')
        self.setGeometry(100, 100, 600, 400)

        # Create a tab widget
        tab_widget = QTabWidget(self)
        self.setCentralWidget(tab_widget)

        # Create tabs
        tab1 = QWidget()
        tab2 = QWidget()

        # Add tabs to the tab widget
        tab_widget.addTab(tab1, 'Tab 1')
        tab_widget.addTab(tab2, 'Tab 2')

        # Set up layout for Tab 1
        layout_tab1 = QVBoxLayout(tab1)

        # Create QTextEdit and QRadioButton
        self.text_edit = QTextEdit()
        self.radio_button = QRadioButton('Show QTextEdit')

        # Connect the radio button's toggled signal to the slot
        self.radio_button.toggled.connect(self.toggle_text_edit)

        # Add widgets to the layout
        layout_tab1.addWidget(self.text_edit)
        layout_tab1.addWidget(self.radio_button)

        # Set up layout for Tab 2
        layout_tab2 = QVBoxLayout(tab2)
        layout_tab2.addWidget(QTextEdit('Content in Tab 2'))

    def toggle_text_edit(self, checked):
        # Toggle the visibility of the QTextEdit based on the radio button state
        self.text_edit.setVisible(checked)

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
