import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QPushButton, QToolButton, QMenu, QLabel, QWidgetAction
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from functools import partial

### Creates a tab that is described in json config file
### 
class createTab(QtWidgets.QMainWindow): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.tab_dict = parent.tab_dict
        self.boxes = self.tab_dict['boxes']
        self.tab_title = self.tab_dict['title']
        self.port = parent.port
        self.statusText = parent.statusBar.statusText
        self.dataEntryButtonClicked = parent.dataEntryButtonClicked
        self.tabWidget = parent.tabWidget
        self.initUI()

    def initUI(self):
        self.buttons = []
        self.entryItem = {}

        self.highlightColor = "yellow"
        self.outlineColor = "white"

        self.widgets = []
        self.widget_index = 0
        self.toolButtonOnIndex = 0  # tracks highlighting buttons in each widget
        self.toolButtonButtons = {}
        self.toolData = {}

        central_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        main_layout.addLayout(layout)

        for box in self.boxes:
            button_rows = box['buttons']
            layout.addWidget(self.createBox(box['name'], button_rows))

        self.widget_index = 0
        self.setCentralWidget(central_widget)

    # keypress events not handled in main are handled here
    def keyPressEvent(self, event):
        key = event.key()

        t = self.widgets[self.widget_index]

        if key == Qt.Key_4:
            print("sub LEFT")
            self.parent.key_sound()
            self.navigateTools(-1)
        elif key == Qt.Key_6:
            print("sub RIGHT")
            self.parent.key_sound()
            self.navigateTools(1)
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.parent.key_sound()
            print("sub open tool")
            self.openTool()
        else:
            super().keyPressEvent(event)

    # changes the values in all the widgets when user hits 'get'
    def updateValuesWithGet(self, struct):
        for n in struct['names']:
            r = self.entryItem.get(n)
            if r is not None:
                if isinstance(r['entry_item'], QtWidgets.QLineEdit):
                    pass
                elif isinstance(r['entry_item'], QtWidgets.QComboBox):
                    pass
                elif isinstance(r['entry_item'], QtWidgets.QToolButton):
                    obj = r['entry_item'].menu()
                    d = self.toolData[obj]
                    value = struct[n]['value']

                    if r.get('round'):
                        value = float(value)
                        rnd = int(r.get('round'))
                        value = round(value, rnd)
                        if rnd == 0:
                            value = int(value)
                        value = str(value)

                    d['tool'].setText(d['name'] + '\n' + value)
                    d['value'] = value
                    d['label'].setText(value)

                else:
                    pass

    def createBox(self, box_name, button_rows):
        group_box = QtWidgets.QGroupBox(box_name)
        group_box_layout = QtWidgets.QVBoxLayout()
        for row in button_rows:
            group_box_layout.addLayout(self.createRow(row))

        group_box.setLayout(group_box_layout)
        return(group_box)

    def createRow(self, row):
        # Create a row with QHBoxLayout
        row_layout = QtWidgets.QHBoxLayout()
        row_layout.setSpacing(0)

        # {'name': 'adc1_max', 'type': 'singleText', 'desc': 'ADC1 max val', 'round': '0'}
        for tool in row:
            if "comboBox" in tool['type']:
                tool['list'] = {int(key): value for key, value in tool['list'].items()}
                entry_item = self.createDropdown(tool['name'], tool['list'], 'None')
            else:
                entry_item = self.createKeypad(tool['name'], '')

            row_layout.addWidget(entry_item)
            self.widgets.append(entry_item)
            entry_item.mousePressEvent = partial(self.toolMousePressEvent, self.widget_index)
            self.widget_index = self.widget_index + 1

            # xxx
            self.entryItem[tool['name']] = {}
            self.entryItem[tool['name']]['entry_item'] = entry_item
            if tool.get('round'):
                self.entryItem[tool['name']]['round'] = tool.get('round')

            row_layout.addSpacing(20)

        row_layout.setAlignment(QtCore.Qt.AlignLeft)
        return(row_layout)

    # connected to tool through mousePressEvent
    def toolMousePressEvent(self, num, event):
        count = 0
        for t in self.widgets:
            if count == num:
                self.widget_index = count
            else:
                pass
            count = count + 1
        self.openTool()

    # this happens when user initially selects the tool
    def openTool(self):
        t = self.widgets[self.widget_index]
        t.showMenu()

    # there are two versions of QToolButtons: a keyboard tool and a dropdown tool 
    def createKeypad(self, button_text, layout_label):
        font = QtGui.QFont()
        font.setPointSize(12)

        tool = QToolButton() 
        tool.setFixedWidth(100)
        tool.setFont(font)
        tool.setStyleSheet("background-color: #808B96;" "border :3px solid #ABB2B9;")

        tool.setText(button_text + '\n' + layout_label)
        tool.setPopupMode(QToolButton.InstantPopup)

        widget = QtWidgets.QWidget(self)
        widget.setStyleSheet("border :1px solid white;")
        widget_menu = QMenu(tool)

        widget_layout = QGridLayout(widget)
        widget_label = QLabel(layout_label)
        widget_layout.addWidget(widget_label, 0, 0, 1, 4)

        d = {'type': 'keypad', 'name': button_text, 'value': layout_label, 'label': widget_label, 'tool': tool}
        self.toolData[widget_menu] = d

        # Adjust spacing between buttons
        widget_layout.setHorizontalSpacing(4)
        widget_layout.setVerticalSpacing(4)

        buttons = []
        keys = [ '7', '8', '9', '<<',
                 '4', '5', '6', 'esc',
                 '1', '2', '3', '',
                 '0', '.', 'set', '']
        row = 1
        col = 0

        for key in keys:
            if key == 'set':
                button = QPushButton("set (s)", self)
            else:
                button = QPushButton(key, self)
            button.clicked.connect(partial(self.keypadButtonClick, key, widget_menu, button))
            button.setStyleSheet("background-color: #808B96;" "border :3px solid #ABB2B9;")
            buttons.append(button)
            if key == '':
                button.hide()
            elif key == 'set':
                widget_layout.addWidget(button, row, col, 1, 2)
            else:
                widget_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.toolButtonButtons[widget_menu] = buttons

        widget_action = QWidgetAction(tool)
        widget_action.setDefaultWidget(widget)
        widget_menu.addAction(widget_action)
        widget_menu.installEventFilter(self) 

        tool.setMenu(widget_menu)
        self.toolButtonOnIndex = 0
        self.toolButtonHighlight(widget_menu)

        return tool

    # basically the same as above except it doesnt have a menu
    # button_text -- appears on top of button
    # keys -- the list of things that go into pull down
    # label -- default thing shown at the top of the list. 
    def createDropdown(self, button_text, keys, default):
        font = QtGui.QFont()
        font.setPointSize(12)

        tool = QToolButton() 
        tool.setFixedWidth(100)
        tool.setFont(font)
        tool.setStyleSheet("background-color: #808B96;" "border :3px solid #ABB2B9;")

        tool.setText(button_text + '\n  ')
        tool.setPopupMode(QToolButton.InstantPopup)

        widget = QtWidgets.QWidget(self)
        widget.setStyleSheet("border :1px solid white;")
        widget_menu = QMenu(tool)

        widget_layout = QGridLayout(widget)
        widget_label = QLabel(default)
        widget_layout.addWidget(widget_label, 0, 0, 1, 4)

        widget_layout.setVerticalSpacing(1)

        d = {'type': 'dropdown', 'name': button_text, 'value': default, 'label': widget_label, 'tool': tool}
        # xxx
        self.toolData[widget_menu] = d

        buttons = []
        row = 1
        # print(f"KEYS {keys}")
        for key, value in keys.items():
            button = QPushButton(value, self)
            button.clicked.connect(partial(self.dropdownButtonClick, key, value, widget_menu, button))
            button.setStyleSheet("background-color: #808B96;" "border :3px solid #ABB2B9;")
            buttons.append(button)
            widget_layout.addWidget(button, row, 0)
            row = row + 1

        self.toolButtonButtons[widget_menu] = buttons

        widget_action = QWidgetAction(tool)
        widget_action.setDefaultWidget(widget)
        widget_menu.addAction(widget_action)
        widget_menu.installEventFilter(self) 

        tool.setMenu(widget_menu)
        self.toolButtonOnIndex = 0

        return tool

    # navigates keys things once the tool is opened
    def eventFilter(self, obj, event):
        d = self.toolData[obj]
        #format:  {'key': button_text, 'value': layout_label, 'label': widget_label}
        label = d['label']

        if event.type() == QEvent.KeyPress:
            if d['type'] == 'keypad':
                self.keypadEvent(obj, event)
            elif d['type'] == 'dropdown':
                self.dropdownEvent(obj, event)

        return super().eventFilter(obj, event)

    # capture events for dropdown tools
    def dropdownEvent(self, obj, event):
        d = self.toolData[obj]
        label = d['label']

        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Up:
                print("2d UP")
                self.toolButtonOnIndex = (self.toolButtonOnIndex - 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Down:
                print("2d DOWN")
                self.toolButtonOnIndex = (self.toolButtonOnIndex + 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Left:
                print("2d LEFT")
                self.toolButtonOnIndex = (self.toolButtonOnIndex - 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Right:
                print("2d RIGHT")
                self.toolButtonOnIndex = (self.toolButtonOnIndex + 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Enter or key == Qt.Key_Return:
                b = self.toolButtonButtons[obj][self.toolButtonOnIndex]
                b.click()
                print("SET {0}".format(self.toolButtonOnIndex))
                d['tool'].setText(d['name'] + '\n' + label.text())
                d['value'] = label.text()
                print(f"set {d['name']} {d['value']}")
                obj.hide()
                return True

    # capture events for keypad tools
    def keypadEvent(self, obj, event):
        d = self.toolData[obj]
        label = d['label']

        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Up:
                if self.toolButtonOnIndex == 3:
                    self.toolButtonOnIndex = 14
                elif self.toolButtonOnIndex == 7:
                    self.toolButtonOnIndex = 3
                elif self.toolButtonOnIndex == 14:
                    self.toolButtonOnIndex = 7
                else:
                    self.toolButtonOnIndex = (self.toolButtonOnIndex - 4) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Down:
                if self.toolButtonOnIndex == 7:
                    self.toolButtonOnIndex = 14
                elif self.toolButtonOnIndex == 14:
                    self.toolButtonOnIndex = 3
                else:
                    self.toolButtonOnIndex = (self.toolButtonOnIndex + 4) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Left:
                self.toolButtonOnIndex = (self.toolButtonOnIndex - 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Right:
                self.toolButtonOnIndex = (self.toolButtonOnIndex + 1) % len(self.toolButtonButtons[obj])
                self.toolButtonHighlight(obj)
            elif key == Qt.Key_Enter or key == Qt.Key_Return:
                b = self.toolButtonButtons[obj][self.toolButtonOnIndex]
                b.click()
                return True
            elif Qt.Key_0 <= key <= Qt.Key_9:
                digit = key - Qt.Key_0
                int_value = int(digit)
                label.setText(label.text() + str(int_value))
            elif key == Qt.Key_Backspace:
                s = label.text()
                label.setText(s[:-1])
            elif key == Qt.Key_Period:
                label.setText(label.text() + '.')
            elif key == Qt.Key_S:
                print("SET")
                d['tool'].setText(d['name'] + '\n' + label.text())
                d['value'] = label.text()
                print(f"set {d['name']} {d['value']}")
                obj.hide()

    # once a tool is open, bops around based on directional keys
    def navigateTools(self, direction):
        self.widget_index = (self.widget_index + direction) % len(self.widgets)

        count = 0
        for t in self.widgets:
            if count == self.widget_index:
                t.setStyleSheet("background-color: #808B96;" "border :3px solid green;")
            else:
                t.setStyleSheet("background-color: #808B96;" "border :3px solid #ABB2B9;")
            count = count + 1

    # comes here if the user has hit a tool button on keypad
    def keypadButtonClick(self, key, obj, button):
        self.toolButtonOnIndex = self.toolButtonButtons[obj].index(button)
        self.toolButtonHighlight(obj)

        d = self.toolData[obj]
        label = d['label']
        try:
            int_value = int(key)
            label.setText(label.text() + str(int_value))
            print(label.text())
        except:
            if key == 'esc':
                obj.hide()
            if key == '<<':
                s = label.text()
                label.setText(s[:-1])
            if key == '.':
                label.setText(label.text() + key)
            # update number for self.toolValues only when return is pressed
            if key == 'set':
                d['tool'].setText(d['name'] + '\n' + label.text())
                d['value'] = label.text()
                print(f"set {d['name']} {d['value']}")
                obj.hide()

    # comes here if the user has hit a tool button on dropdown
    def dropdownButtonClick(self, key, value, obj, button):
        self.toolButtonOnIndex = self.toolButtonButtons[obj].index(button)
        self.toolButtonHighlight(obj)

        d = self.toolData[obj]

        d['tool'].setText(d['name'] + '\n' + value)
        d['value'] = value
        print(f"set {d['name']} {key} {obj}")

        obj.hide()

    # shows if a button on tool was selected
    def toolButtonHighlight(self, obj):
        for n, b in enumerate(self.toolButtonButtons[obj]):
            if n == self.toolButtonOnIndex:
                b.setStyleSheet("background-color: #808B96;" "border :3px solid green;")
            else:
                b.setStyleSheet("background-color: #808B96;" "border :3px solid #ABB2B9;")
                
