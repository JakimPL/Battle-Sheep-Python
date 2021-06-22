import pygame
from pygame import locals


class Mouse:
    def __init__(self):
        self._position = None
        self._previous_state = False
        self._state = False
        self._wheel = 0

    def update(self, wheel=0):
        self._previous_state = self._state
        self._state = pygame.mouse.get_pressed(3)[0]
        self._position = pygame.mouse.get_pos()
        self._wheel = wheel

    def position(self):
        return self._position

    def pressed(self):
        return self._state and not self._previous_state

    def released(self):
        return self._previous_state and not self._state

    def wheel(self):
        return self._wheel
