import random

DIRECTIONS = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]


class Tile:
    player = 0
    value = 0

    def __init__(self, player, value):
        self.player = player
        self.value = value

    def __iter__(self):
        return iter((self.player, self.value))


class Board:
    def __init__(self, board=None, block_size=2):
        self._board = board if board else {}
        self._block_size = block_size

    def __call__(self, tile) -> Tile:
        return self._board[tile]

    def __iter__(self):
        return self._board.__iter__()

    def get_block_size(self):
        return self._block_size

    def get_adjacent_tiles(self, tile, external=False):
        x, y = tile
        adjacent_tiles = []
        for new_tile in [(x - 1, y + 1), (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x + 1, y - 1)]:
            if (new_tile in self._board) ^ external:
                adjacent_tiles.append(new_tile)
        return adjacent_tiles

    def get_tiles_in_direction(self, starting_tile,  direction):
        tile = (starting_tile[0] + direction[0], starting_tile[1] + direction[1])
        tiles = []
        while self.is_tile_free(tile):
            tiles.append(tile)
            tile = (tile[0] + direction[0], tile[1] + direction[1])

        return tiles

    def is_tile_boundary(self, tile):
        return len(self.get_adjacent_tiles(tile)) < 6

    def is_tile_free(self, tile):
        if tile in self._board:
            return self._board[tile].player == 0

        return False

    def is_tile_movable(self, tile):
        if tile in self._board:
            player, value = self._board[tile]
            return player > 0 and value > 1

        return False

    def is_block_inside(self, tile, outside=False):
        x, y = tile
        for i in range(self._block_size):
            for j in range(self._block_size):
                if outside ^ ((x + i, y + j) in self._board):
                    return False

        return True

    def get_random_block(self):
        boundary_blocks = set()
        for tile in self._board:
            if self.is_tile_boundary(tile):
                x, y = tile
                block_lists = \
                    [(x - self._block_size + i + 1, y - self._block_size) for i in range(self._block_size + 1)] + \
                    [(x - self._block_size, y - self._block_size + i + 1) for i in range(self._block_size + 1)] + \
                    [(x + 1, y - self._block_size + i) for i in range(1, self._block_size + 1)] + \
                    [(x - self._block_size + i, y + 1) for i in range(1, self._block_size + 1)]

                for block in block_lists:
                    if self.is_block_inside(block, outside=False):
                        boundary_blocks.add(block)

        return random.choice(list(boundary_blocks))

    def generate_board(self, blocks):
        block_tiles = self._block_size * self._block_size
        if blocks % block_tiles != 0:
            raise ValueError('number of blocks is not divisible by the size of the block')

        self.fill_block((0, 0))
        remaining_blocks = blocks - block_tiles
        while remaining_blocks > 0:
            block = self.get_random_block()
            self.fill_block(block)
            remaining_blocks -= block_tiles

        if len(self._board) != blocks:
            raise RuntimeError('generated smaller board than expected')

    def set(self, tile, value=Tile(0, 0)):
        self._board[tile] = value

    def fill_block(self, tile, value=Tile(0, 0)):
        x, y = tile
        for i in range(self._block_size):
            for j in range(self._block_size):
                self.set((x + i, y + j), value)

    def is_connected(self):
        pass
