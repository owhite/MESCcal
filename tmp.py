#!/usr/bin/env python3

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QToolBar


class FileListTab(QWidget):
    def __init__(self, file_list):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.label = QLabel("", self)
        self.layout.addWidget(self.label)

        # self.update_value(file_list)

    def update_value(self, file_list):
        self.label.setText("\n".join(file_list))


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()

        self.create_toolbar()

        # Initialize tabs with empty widgets
        self.tab1 = FileListTab([])
        self.tab2 = FileListTab([])
        self.tabs.addTab(self.tab1, "First Half")
        self.tabs.addTab(self.tab2, "Second Half")

        self.setCentralWidget(self.tabs)

    def create_toolbar(self):
        toolbar = QToolBar("File Toolbar", self)
        self.addToolBar(toolbar)

        run_ls_action = toolbar.addAction("Run ls Command")
        run_ls_action.triggered.connect(self.run_ls_command)

    def run_ls_command(self):
        directory_path = "."  # Change this to the desired directory path
        result = subprocess.run(["ls", directory_path], capture_output=True, text=True)

        if result.returncode == 0:
            file_list = result.stdout.splitlines()
            half_length = len(file_list) // 2

            first_half_list = file_list[:half_length]
            second_half_list = file_list[half_length:]

            # Update the existing widgets in the tabs
            self.tab1.update_value(first_half_list)
            self.tab2.update_value(second_half_list)


def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
