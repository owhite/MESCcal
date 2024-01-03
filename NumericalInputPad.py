import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout

### I simply can not believe how easy it was to implement full touch input. 
###
class NumericalInputPad(QWidget):
    def __init__(self, app_self, name, value):
        self.name = name
        self.value = value
        self.app = app_self
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Touchpad')
        self.setGeometry(self.app.geometry().topLeft().x(), self.app.geometry().topLeft().y(), 10, 200)  

        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(5, 5, 5, 5)

        label1_layout = QHBoxLayout()
        label1_layout.setSpacing(2)

        self.input_line_edit = QLineEdit(self)
        self.input_line_edit.setFixedWidth(120) 

        if not self.app.port.isOpen():
            self.app.statusBar.statusText.setText('Port closed: cant update')
            label = QLabel('Port closed cant update')
            label1_layout.addWidget(label)
            main_layout.addLayout(label1_layout)
        else:
            label = QLabel('set ' + self.name + " ")
            label1_layout.addWidget(label)
            label1_layout.addWidget(self.input_line_edit)
            main_layout.addLayout(label1_layout)

            label2_layout = QHBoxLayout()
            label2_layout.setSpacing(2)
            if len(self.value) > 0:
                label = QLabel('was: ' + str(self.value))
            else:
                label = QLabel('was: empty')
            label2_layout.addWidget(label)
            main_layout.addLayout(label2_layout)

        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(2)
        buttons = [
            '7', '8', '9', '<<',
            '4', '5', '6', 'cancel',
            '1', '2', '3', 'enter',
            '', '0', '.', ''
        ]

        row = 0
        col = 0

        for button_text in buttons:
            button = QPushButton(button_text, self)
            button.clicked.connect(lambda _, text=button_text: self.on_button_click(text))
            if button_text == '':
                button.hide()
            elif button_text == 'enter':
                # Make the 'enter' button span two rows
                button.setFixedHeight(60)
                buttons_layout.addWidget(button, row, col, 2, 1)
            else:
                buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        buttons_layout.setHorizontalSpacing(2)
        buttons_layout.setVerticalSpacing(2) 
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def on_button_click(self, text):
        if text == '<<':
            current_text = self.input_line_edit.text()
            self.input_line_edit.setText(current_text[:-1])
        elif text == 'enter':
            print("ENTER")
            n = self.input_line_edit.text()
            if self.isIntOrFloat(n):
                text = 'set {0} {1}'.format(self.name, n)
                self.app.statusBar.statusText.setText(text)
                text = text + '\r\n'
                self.app.port.write( text.encode() )
            else:
                self.app.statusBar.statusText.setText('{0} not number'.format(n))

        elif text == 'cancel':
            self.close()
        else:
            # Append the clicked button text to the input line edit
            current_text = self.input_line_edit.text()
            self.input_line_edit.setText(current_text + text)

    def isIntOrFloat(self, s):
        try:
            int_value = int(s)
            return True
        except ValueError:
            try:
                float_value = float(s)
                return True
            except ValueError:
                return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    numerical_input_pad = NumericalInputPad('input_opt', 20, 'thing')
    numerical_input_pad.show()
    sys.exit(app.exec_())
