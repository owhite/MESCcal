#!/usr/bin/env python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # stop annoying messages
import pygame

class keySound():
    def __init__(self, parent):
        self.parent = parent
        self.keyPressSound = [False]  # Initialize the list with a default value
        pygame.mixer.init(channels=1, buffer=1024)
        pygame.mixer.music.load('./soundfile.wav')

    def key_sound(self, new_value):
        print(new_value)
        if new_value:
            pygame.mixer.music.play()

# Now, when you create an instance of keySound, it should work as expected
keyPressSound = [False]
sound = keySound(keyPressSound)
keyPressSound[0] = True
sound.key_sound(keyPressSound[0])
