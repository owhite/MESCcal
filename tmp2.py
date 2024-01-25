#!/usr/bin/env python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class SoundPlayerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create a QPushButton
        btn_play_sound = QPushButton('Play Sound', self)

        # Connect the button's click event to the play_sound method
        btn_play_sound.clicked.connect(self.play_sound)

        # Create a vertical layout and add the button to it
        layout = QVBoxLayout(self)
        layout.addWidget(btn_play_sound)

        # Set the layout for the main window
        self.setLayout(layout)

        pygame.mixer.init(channels=1, buffer=1024)
        pygame.mixer.music.load('/Users/owhite/MESCcal/soundfile.wav')

        # Set the window properties
        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle('Sound Player App')
        self.show()

    def play_sound(self):
        # Initialize Pygame mixer
        pygame.mixer.music.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SoundPlayerApp()
    sys.exit(app.exec_())
