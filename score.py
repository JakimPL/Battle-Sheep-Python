class Score:
    def __init__(self):
        self.tiles = 0
        self.max_component = 0

    def __iter__(self):
        return iter((self.tiles, self.max_component))

    def __repr__(self):
        return "{0}, {1}".format(self.tiles, self.max_component)

    def __eq__(self, other):
        return self.tiles == other.tiles and self.max_component == other.max_component

    def __lt__(self, other):
        return self.tiles < other.tiles or (self.tiles == other.tiles and self.max_component < other.max_component)

    def __gt__(self, other):
        return self.tiles > other.tiles or (self.tiles == other.tiles and self.max_component > other.max_component)
