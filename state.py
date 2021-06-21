import random


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

    def __call__(self, tile: Tile):
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

    def is_tile_boundary(self, tile):
        return len(self.get_adjacent_tiles(tile)) < 6

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


class State:
    def __init__(self, players: int, board=None, stack_size=16):
        if players < 1:
            raise ValueError('not enough players')

        self.players = players
        self.stack_size = stack_size

        self.turn = 1
        self.initial_phase = True
        if board is None:
            self.board = Board()
            self.board.generate_board(self.players * self.stack_size)
        else:
            self.board = Board(board)

    def place_initial_stack(self, tile):
        if self.initial_phase and tile in self.board and self.board(tile).player == 0 \
                and self.board.is_tile_boundary(tile):
            self.board.set(tile, Tile(self.turn, self.stack_size))
            self.next_turn()
            if self.turn == 1:
                self.initial_phase = False

    def next_turn(self):
        self.turn += 1
        if self.turn > self.players:
            self.turn -= self.players
