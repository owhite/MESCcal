from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # stop annoying messages
import pygame

class keySound():
    def __init__(self):
        pygame.mixer.init(channels=1, buffer=1024)
        pygame.mixer.music.load('./soundfile.wav')

    def key_sound(self, t):
        if t:
            pygame.mixer.music.play()


