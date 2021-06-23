import itertools
import random
from config import Config

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
    config = Config('game')

    def __init__(self, board=None, block_size=config['block_size']):
        self._board = {}
        if board:
            if type(board) == dict:
                for tile in board:
                    player, value = board[tile]
                    self._board[tile] = Tile(player, value)
            elif type(board) == list:
                for tile in board:
                    self._board[tile] = Tile(0, 0)

        self._block_size = block_size

    def __call__(self, tile) -> Tile:
        return self._board[tile]

    def __iter__(self):
        return self._board.__iter__()

    def __len__(self):
        return len(self._board)

    def get_block_size(self):
        return self._block_size

    def get_adjacent_tiles(self, tile, external=False):
        x, y = tile
        adjacent_tiles = []
        for a, b in DIRECTIONS:
            new_tile = x + a, y + b
            if (new_tile in self._board) ^ external:
                adjacent_tiles.append(new_tile)
        return adjacent_tiles

    def get_list(self):
        board = []
        for tile in self._board:
            player, value = self._board[tile]
            board.append({'tile': [tile[0], tile[1]], 'player': player, 'value': value})
        return board

    def get_size(self):
        return len(self._board)

    def get_tiles_in_direction(self, starting_tile,  direction):
        tile = (starting_tile[0] + direction[0], starting_tile[1] + direction[1])
        tiles = []
        while self.is_tile_free(tile):
            tiles.append(tile)
            tile = (tile[0] + direction[0], tile[1] + direction[1])

        return tiles

    def get_connected_components(self):
        count = 0
        components = []
        visited_tiles = {}

        size = self.get_size()
        if size == 0:
            return components

        while count < size:
            first_tile = next(iter([tile for tile in self._board if tile not in visited_tiles]))
            player = self._board[first_tile].player
            tiles = [first_tile]
            component = []
            while tiles:
                new_tiles = []
                for tile in tiles:
                    if tile not in visited_tiles:
                        component.append(tile)
                        count += 1
                        visited_tiles[tile] = True
                        new_tiles += [adjacent_tile for adjacent_tile in self.get_adjacent_tiles(tile) if self._board[adjacent_tile].player == player]
                tiles = new_tiles
            components += [component]

        return components

    def get_connected_component_size(self, tile=None, player=-1):
        if self.get_size() == 0:
            return True

        first_tile = next(iter(self._board)) if tile is None else tile

        count = 0
        visited_tiles = {}
        tiles = [first_tile]
        while tiles:
            new_tiles = []
            for tile in tiles:
                if tile not in visited_tiles:
                    count += 1
                    visited_tiles[tile] = True
                    new_tiles += [adjacent_tile for adjacent_tile in self.get_adjacent_tiles(tile) if self._board[adjacent_tile].player == player or player < 0]

            tiles = new_tiles

        return count

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

    def is_block_inside(self, tile, outside=False, transpose=False):
        tiles = self.get_block(tile, transpose=transpose)
        for tile in tiles:
            if outside ^ (tile in self._board):
                return False

        return True

    def get_boundary_blocks(self, tile, transpose=False):
        x, y = tile
        b = self._block_size
        if transpose:
            return [(x + i, y - b) for i in range(b + 1)] + \
                    [(x - i, y - b + i) for i in range(1, b + 1)] + \
                    [(x - b + i, y + 1) for i in range(b + 1)] + \
                    [(x + i, y + 1 - i) for i in range(1, b + 1)]
        else:
            return [(x - b + i + 1, y - b) for i in range(b + 1)] + \
                   [(x - b, y - b + i + 1) for i in range(b + 1)] + \
                   [(x + 1, y - b + i) for i in range(1, b + 1)] + \
                   [(x - b + i, y + 1) for i in range(1, b + 1)]

    def get_random_block(self):
        boundary_blocks = set()
        for tile in self._board:
            for transpose in [False, True]:
                if self.is_tile_boundary(tile):
                    block_lists = self.get_boundary_blocks(tile, transpose=transpose)
                    for block in block_lists:
                        if self.is_block_inside(block, outside=False, transpose=transpose):
                            boundary_blocks.add((block, transpose))

        return random.choice(list(boundary_blocks))

    def generate_board(self, blocks):
        block_tiles = self._block_size * self._block_size
        if blocks % block_tiles != 0:
            raise ValueError('number of blocks is not divisible by the size of the block')

        self.fill_block((0, 0), transpose=(random.random() < 0.5))
        remaining_blocks = blocks - block_tiles
        while remaining_blocks > 0:
            block, transpose = self.get_random_block()
            self.fill_block(block, transpose=transpose)
            remaining_blocks -= block_tiles

        if len(self._board) != blocks:
            raise RuntimeError('generated smaller board than expected')

    def set(self, tile, value=Tile(0, 0)):
        self._board[tile] = value

    def get_block(self, tile, transpose=False):
        x, y = tile
        if transpose:
            tiles = [[(x + i - j, y + j) for i in range(self._block_size)] for j in range(self._block_size)]
        else:
            tiles = [[(x + i, y + j) for i in range(self._block_size)] for j in range(self._block_size)]

        return list(itertools.chain.from_iterable(tiles))

    def fill_block(self, tile, value=Tile(0, 0), transpose=False):
        tiles = self.get_block(tile, transpose=transpose)
        for tile in tiles:
            self.set(tile, value)
