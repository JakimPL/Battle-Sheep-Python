class Board:
    def __init__(self):
        self._board = {}

    def __call__(self, tile):
        return self._board[tile]

    def __iter__(self):
        return self._board.__iter__()

    def get_adjacent_tiles(self, tile, external=False):
        x, y = tile
        adjacent_tiles = []
        for new_tile in [(x - 1, y - 1), (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x + 1, y + 1)]:
            if (new_tile in self._board) ^ external:
                adjacent_tiles.append(new_tile)
        return adjacent_tiles

    def is_tile_boundary(self, tile):
        return len(self.get_adjacent_tiles(tile, False)) == 0

    def generate_random(self, blocks, block_size=(2, 2)):
        if blocks % (block_size[0] * block_size[1]) != 0:
            raise ValueError('number of blocks is not divisible by the size of the block')

        for i in range(block_size[0]):
            for j in range(block_size[1]):
                self._board[(i, j)] = 0
        remaining_blocks = blocks - block_size[0] * block_size[1]

        boundary_tiles = []
        for tile in self._board:
            if self.is_tile_boundary(tile):
                boundary_tiles.append(tile)

    def is_connected(self):
        pass


class State:
    def __init__(self, players: int, board=None):
        if players < 1:
            raise ValueError('not enough players')

        self.players = players
        self.turn = 1
        if board is None:
            self.board = Board()
            self.board.generate_random(self.players * 4)
        else:
            self.board = board
