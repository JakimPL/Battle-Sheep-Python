class Mouse:
    def __init__(self):
        self._previous_state = False
        self._state = False

    def update(self, state: bool):
        self._previous_state = self._state
        self._state = state

    def pressed(self):
        return self._state and not self._previous_state

    def released(self):
        return self._previous_state and not self._state
