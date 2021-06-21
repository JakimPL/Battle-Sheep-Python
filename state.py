from board import Board, Tile


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
