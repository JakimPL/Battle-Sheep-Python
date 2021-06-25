from board import Board, Tile, DIRECTIONS
from config import Config


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


class State:
    config = Config('game')

    def __init__(self, players=config['players'], board=None, stack_size=config['stack_size']):
        if players < 1:
            raise ValueError("not enough players")

        self.players = players
        self.stack_size = stack_size

        self.turn = 0
        self.end = False
        if board is None:
            self.board = Board()
            self.board.generate_board(self.players * self.stack_size)
        else:
            self.board = Board(board)

        board_size = self.board.get_size()
        if self.players > board_size:
            raise ValueError("not enough space for players")

        if self.config['check_connectedness'] and self.board.get_connected_component_size() != self.board.get_size():
            raise ValueError("board is not connected")

        player_tiles = [tile for tile in self.board if self.board(tile).player > 0]
        if player_tiles:
            players = set()
            board_stack_size = self.board(player_tiles[0]).value
            self.initial_phase = False
            max_player = 0
            for tile in player_tiles:
                player, value = self.board(tile)
                players.add(player)
                if len(player_tiles) == self.players and value != board_stack_size:
                    raise ValueError("uneven stack size: {0} versus {1}".format(value, board_stack_size))
                if player > max_player:
                    max_player = player

            players_count = len(players)
            if players_count != self.players:
                raise ValueError("wrong number of players: {0} instead of {1}".format(players_count, self.players))
            if players_count != max_player:
                raise ValueError("at least one player is not present")
        else:
            self.initial_phase = True

        for tile in self.board:
            player, value = self.board(tile)
            if value < 0:
                raise ValueError("negative value of quantity")
            if player == 0 and value != 0:
                raise ValueError("there is a neutral tile with non-zero quantity")
            elif player > 0 and value == 0:
                raise ValueError("there is a player's tile with zero quantity")

        self.score = self.calculate_score()
        self.winners = []
        self.next_turn()

    def __iter__(self):
        yield 'stack_size', self.stack_size
        yield 'players', self.players
        yield 'turn', self.turn
        yield 'initial_phase', self.initial_phase
        yield 'end', self.end
        yield 'board', self.board.get_list()

    def _end(self):
        self.board.get_connected_components()
        self.turn = 0
        self.end = True

        self.score = self.calculate_score()
        max_score = max([self.score[score] for score in self.score])
        self.winners = [player for player in self.score if self.score[player] == max_score]

    def calculate_score(self):
        counter = {player: Score() for player in range(1, self.players + 1)}
        for tile in self.board:
            player, value = self.board(tile)
            if player > 0:
                counter[player].tiles += 1

        components = self.board.get_connected_components()
        for component in components:
            component_size = len(component)
            player = self.board(component[0]).player
            if player > 0 and component_size > counter[player].max_component:
                counter[player].max_component = component_size

        return counter

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
            if self.turn == self.players:
                self.initial_phase = False

            self.next_turn()

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

        self._end()
        return True
