import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QCheckBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal

# HL = "Hightlightable"
class HLCheckBox(QObject):
    highlighted = pyqtSignal(bool)
    checkBoxStateChanged = pyqtSignal(bool)  # Signal to indicate checkbox state change

    def __init__(self, checkbox):
        super(HLCheckBox, self).__init__()
        self.checkBox = checkbox
        self.highlighted.connect(self.setHighlighted)
        self.checkBox.setFocusPolicy(Qt.StrongFocus)
        # self.checkBox.installEventFilter(self)
        self.isHighlighted = False

    def setHighlighted(self, highlighted):
        self.isHighlighted = highlighted

    def eventFilter(self, obj, event):
        print("NEVER1")
        return super(HLCheckBox, self).eventFilter(obj, event)

        if obj == self.checkBox:
            if event.type() == event.FocusIn:
                self.highlighted.emit(True)
                self.checkBox.setStyleSheet("background-color: yellow;")
            elif event.type() == event.FocusOut:
                self.highlighted.emit(False)
                self.checkBox.setStyleSheet("")
            elif event.type() == event.KeyPress and self.isHighlighted:
                key = event.key()
                print(f'Key Pressed: {key}')
                if event.key() == Qt.Key_Return:
                    print("BOINK")
                    self.checkBox.setChecked(not self.checkBox.isChecked())
                    # Emit the signal
                    self.checkBoxStateChanged.emit(self.checkBox.isChecked()) 
            elif event.type() == event.MouseButtonPress and self.isHighlighted:
                self.checkBox.setChecked(not self.checkBox.isChecked())
                self.checkBoxStateChanged.emit(self.checkBox.isChecked()) 

        return super(HLCheckBox, self).eventFilter(obj, event)

class HLButton(QObject):
    highlighted = pyqtSignal(bool)
    buttonPressed = pyqtSignal()  # Signal to indicate a button press

    def __init__(self, button):
        super(HLButton, self).__init__()
        self.button = button
        self.highlighted.connect(self.setHighlighted)
        self.button.setFocusPolicy(Qt.StrongFocus)
        self.button.setAutoDefault(True)
        # self.button.installEventFilter(self)
        self.isHighlighted = False

    def setHighlighted(self, highlighted):
        print("BUTTON HIGHLIGHT")
        self.isHighlighted = highlighted

    def eventFilter(self, obj, event):
        print("NEVER2")
        return super(HLButton, self).eventFilter(obj, event)

        if obj == self.button:
            if event.type() == event.FocusIn:
                self.highlighted.emit(True)
                self.button.setStyleSheet("background-color: yellow;")
            elif event.type() == event.FocusOut:
                self.highlighted.emit(False)
                self.button.setStyleSheet("")
            elif event.type() == event.KeyPress and self.isHighlighted:
                key = event.key()
                print(f'Key Pressed: {key}')
                if event.key() == Qt.Key_Return:
                    print("BOINK")
                    self.buttonPressed.emit()  # Emit the button press signal
            elif event.type() == event.MouseButtonPress and self.isHighlighted:
                print("MOUSE")
                self.buttonPressed.emit()  # Emit the button press signal

        return super(HLButton, self).eventFilter(obj, event)

class HLLineEdit(QObject):
    highlighted = pyqtSignal(bool)
    lineEditFocused = pyqtSignal()  # Signal to indicate line edit focus

    def __init__(self, line_edit, navigation_widgets):
        super(HLLineEdit, self).__init__()
        self.lineEdit = line_edit
        self.highlighted.connect(self.setHighlighted)
        self.lineEdit.setFocusPolicy(Qt.StrongFocus)
        # self.lineEdit.installEventFilter(self)
        self.navigation_widgets = navigation_widgets
        self.isHighlighted = False

    def setHighlighted(self, highlighted):
        self.isHighlighted = highlighted

    def eventFilter(self, obj, event):
        print("NEVER3")
        return super(HLLineEdit, self).eventFilter(obj, event)

        if obj == self.lineEdit:
            print("IN LineEdit")
            if event.type() == event.FocusIn:
                self.highlighted.emit(True)

            elif event.type() == event.FocusOut:
                self.highlighted.emit(False)
                self.lineEdit.setStyleSheet("")
            elif event.type() == event.KeyPress and self.isHighlighted:
                print("here")
                key = event.key()
                print(f'Key Pressed: {key}')  # Print the key code
                if event.key() == Qt.Key_Left:
                    self.setFocusToPreviousWidget()
                elif event.key() == Qt.Key_Right:
                    self.setFocusToNextWidget()

            # Add more event handling as needed

        return super(HLLineEdit, self).eventFilter(obj, event)

class HLComboBox(QObject):
    highlighted = pyqtSignal(bool)
    lineEditFocused = pyqtSignal()  # Signal to indicate line edit focus

    def __init__(self, combobox, navigation_widgets):
        super(HLComboBox, self).__init__()
        self.combobox = combobox
        self.highlighted.connect(self.setHighlighted)
        self.combobox.setFocusPolicy(Qt.StrongFocus)
        # self.combobox.installEventFilter(self)
        self.navigation_widgets = navigation_widgets
        self.isHighlighted = False

    def setHighlighted(self, highlighted):
        self.isHighlighted = highlighted

    def eventFilter(self, obj, event):
        print("NEVER4")
        return super(HLComboBox, self).eventFilter(obj, event)

        if obj == self.combobox:
            print("IN combobox")
            if event.type() == event.FocusIn:
                self.highlighted.emit(True)
            elif event.type() == event.FocusOut:
                self.highlighted.emit(False)
                self.lineEdit.setStyleSheet("")
            elif event.type() == event.KeyPress and self.isHighlighted:
                print("combobox event filter here")
                key = event.key()
                print(f'Key Pressed: {key}')  # Print the key code
                if event.key() == Qt.Key_Left:
                    self.setFocusToPreviousWidget()
                elif event.key() == Qt.Key_Right:
                    self.setFocusToNextWidget()

        return super(HLComboBox, self).eventFilter(obj, event)
        
