from board import Board, Tile, DIRECTIONS


class State:
    def __init__(self, players: int, board=None, stack_size=16):
        if players < 1:
            raise ValueError('not enough players')

        self.players = players
        self.stack_size = stack_size

        self.turn = 1
        self.initial_phase = True
        self.end = False
        if board is None:
            self.board = Board()
            self.board.generate_board(self.players * self.stack_size)
        else:
            self.board = Board(board)

    def get_possible_moves(self, chosen_tile=None, player=0):
        if player == 0:
            player = self.turn
        if chosen_tile is not None:
            tiles = [chosen_tile] if chosen_tile in self.board else []
        else:
            tiles = [tile for tile in self.board if self.board.is_tile_movable(tile)]

        possible_moves = []
        for tile in [tile for tile in tiles if self.board(tile).player == player]:
            for adjacent_tile in self.board.get_adjacent_tiles(tile):
                if adjacent_tile in self.board and self.board(adjacent_tile).player == 0:
                    possible_moves.append(adjacent_tile)

        return possible_moves

    def place_initial_stack(self, tile):
        if self.initial_phase and self.board.is_tile_free(tile) and self.board.is_tile_boundary(tile):
            self.board.set(tile, Tile(self.turn, self.stack_size))
            self.next_turn()
            if self.turn == 1:
                self.initial_phase = False

    def move(self, starting_tile, direction, size=1):
        if direction not in DIRECTIONS:
            raise ValueError("wrong direction: {0}".format(direction))
        if not self.board.is_tile_movable(starting_tile):
            raise ValueError("stack is not movable")
        if starting_tile in self.board and self.board(starting_tile).player == self.turn:
            tiles_in_direction = self.board.get_tiles_in_direction(starting_tile, direction)
            if tiles_in_direction:
                ending_tile = tiles_in_direction[-1]
                self.board.set(ending_tile, Tile(self.turn, size))
                self.board.set(starting_tile, Tile(self.turn, self.board(starting_tile).value - size))
                self.next_turn()
            else:
                raise ValueError("move is not possible in chosen direction")
        else:
            raise ValueError("starting position is not of the current player")

    def next_turn(self) -> bool:
        counter = 0
        while counter < self.players:
            self.turn += 1
            if self.turn > self.players:
                self.turn -= self.players
            if self.initial_phase or self.get_possible_moves():
                return False
            else:
                counter += 1
        self.end = True
        return True
