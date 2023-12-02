#!/usr/bin/env python3


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QToolBar, QAction, QHBoxLayout

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create main widget and set layout
        main_widget = QtWidgets.QWidget(self)
        main_layout = QHBoxLayout(main_widget)
        main_widget.setLayout(main_layout)

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

        # Create a toolbar
        toolbar = QToolBar("My Toolbar", self)
        self.addToolBar(toolbar)

        # Create a button on the toolbar
        open_panel_action = QAction("Toggle Panel", self)
        open_panel_action.triggered.connect(self.toggle_panel)
        toolbar.addAction(open_panel_action)

        # Create a container widget for the panels
        self.panel_container = QWidget(self)
        self.panel_layout = QVBoxLayout(self.panel_container)

        # Add the tab widget and panel container to the main layout
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(self.panel_container)
        self.panel_container.hide()

        # Set central widget
        self.setCentralWidget(main_widget)

        # Set window properties
        self.setWindowTitle("PyQt5 Tabs, Toolbar, and Dynamic Right Panel Example")
        self.setGeometry(100, 100, 800, 600)

    def toggle_panel(self):
        window_size = window.size()

        if self.panel_container.isHidden():
            self.panel_container.show()
            self.panel_container.setFixedWidth(200)
            self.last_width = window_size.width()
            self.setGeometry(100, 100, window_size.width()+200, 600)
        else:
            self.setGeometry(100, 100, self.last_width, 600)
            self.panel_container.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
