import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create central widget
        central_widget = QWidget()

        # Create a QGroupBox for buttons
        group_box1 = QGroupBox("Vertical Buttons")

        # Create three QPushButton instances for the first row
        h1_button1 = QPushButton("V Button 1")
        h1_button2 = QPushButton("V Button 2")
        h1_button3 = QPushButton("V Button 3")
        h1_button1.setFixedWidth(100)
        h1_button2.setFixedWidth(100)
        h1_button3.setFixedWidth(100)

        le1_1 = QLineEdit()
        le1_1.setFixedWidth(100)

        # Create three QPushButton instances for the second row
        h2_button1 = QPushButton("V Button 4")
        h2_button2 = QPushButton("V Button 5")
        h2_button3 = QPushButton("V Button 6")
        h2_button1.setFixedWidth(100)
        h2_button2.setFixedWidth(100)
        h2_button3.setFixedWidth(100)

        # Create a QHBoxLayout for the buttons in the first row
        row1_layout = QHBoxLayout()
        row1_layout.addWidget(h1_button1)
        row1_layout.addWidget(le1_1)
        row1_layout.addWidget(h1_button2)
        row1_layout.addWidget(h1_button3)
        row1_layout.setAlignment(Qt.AlignLeft)

        # Create a QHBoxLayout for the buttons in the second row
        row2_layout = QHBoxLayout()
        row2_layout.addWidget(h2_button1)
        row2_layout.addWidget(h2_button2)
        row2_layout.addWidget(h2_button3)
        row2_layout.setAlignment(Qt.AlignLeft)

        # Create a QVBoxLayout for the main layout and add the two rows
        group_box1_layout = QVBoxLayout()
        group_box1_layout.addLayout(row1_layout)
        group_box1_layout.addLayout(row2_layout)

        group_box1.setLayout(group_box1_layout)


        # Create a layout for the central widget and add the QLabel and both QGroupBoxes
        central_widget_layout = QVBoxLayout()
        central_widget_layout.addWidget(group_box1)
        central_widget.setLayout(central_widget_layout)

        # Set the central widget for the main window
        self.setCentralWidget(central_widget)

        # Set window properties
        self.setWindowTitle("PyQt5 Central Widget Example")
        self.setGeometry(100, 100, 600, 300)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
