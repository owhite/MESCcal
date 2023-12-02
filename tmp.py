#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create main widget and set layout
        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)
        main_widget.setLayout(main_layout)

        # Create left panel with tabs and status bar
        left_panel = QWidget(self)
        left_layout = QVBoxLayout(left_panel)
        left_panel.setLayout(left_layout)

        # Create tab widget
        tab_widget = QTabWidget(self)

        # Create tabs
        tab1 = QWidget(self)
        tab2 = QWidget(self)
        tab3 = QWidget(self)

        # Add tabs to tab widget
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")
        tab_widget.addTab(tab3, "Tab 3")

        # Create status bar
        status_bar = QLabel("Status Bar", self)

        # Add the tab widget and status bar to the left layout
        left_layout.addWidget(tab_widget)
        left_layout.addWidget(status_bar)

        # Create right panel with QTextEdit
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)
        right_panel.setLayout(right_layout)

        text_edit = QTextEdit(self)
        right_layout.addWidget(text_edit)

        # Add the left and right panels to the main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        # Set central widget
        self.setCentralWidget(main_widget)

        # Set window properties
        self.setWindowTitle("PyQt5 Two Panels Example")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
