#!/usr/bin/env python3

import pyqtcss
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("Hello, PyQt5!")

# pyqtcss.available_styles() = ['classic', 'dark_blue', 'dark_orange']

style_string = pyqtcss.get_style("dark_blue")
label.setStyleSheet(style_string)

label.show()
app.exec_()
