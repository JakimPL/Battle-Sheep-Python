class Mouse:
    def __init__(self):
        self._position = (0, 0)
        self._previous_state = False
        self._state = False
        self._wheel = 0

    def kivy_frame(self):
        self._wheel = 0
        self._previous_state = self._state
        self._state = False

    def kivy_update_position(self, etype, motionevent):
        if etype:
            self._position = motionevent

    def kivy_update_state(self, instance, touch):
        try:
            if touch.button == 'left':
                self._state = True
        except AttributeError:
            pass

        if touch.is_mouse_scrolling:
            self._wheel = 1 if touch.button == 'scrolldown' else -1

    def pygame_update(self, wheel=0):
        '''
        self._previous_state = self._state

        #self._state = pygame.mouse.get_pressed(3)[0]
        #self._position = pygame.mouse.get_pos()

        self._wheel = wheel
        '''

    def position(self):
        return self._position

    def pressed(self):
        return self._state and not self._previous_state

    def released(self):
        return self._previous_state and not self._state

    def wheel(self):
        return self._wheel
