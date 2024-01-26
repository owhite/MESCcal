#!/usr/bin/env python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Demo(QWidget):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        self.toggle = [False]  # Use a list to hold a mutable object

        data_dict = {}
        data_dict['value'] = self.toggle

        # This is the value before the change
        print(self.toggle[0])

        # Change self.toggle using the dictionary reference
        self.change_value(data_dict)

        # self.toggle should now be True
        print(self.toggle[0])

    def change_value(self, d):
        d['value'][0] = True  # Modify the mutable object inside the list

def main():
    app = QApplication(sys.argv)
    ex = Demo()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
