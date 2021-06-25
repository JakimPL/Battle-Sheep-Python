class Tile:
    player = 0
    value = 0

    def __init__(self, player, value):
        self.player = player
        self.value = value

    def __iter__(self):
        return iter((self.player, self.value))

    def __repr__(self):
        return "{0}, {1}".format(self.player, self.value)
