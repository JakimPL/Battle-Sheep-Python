from board import Tile
from mouse import Mouse
from state import State
from ui import UI
import json
import pygame
import re
import sys
from pygame import locals


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.state = State()
        self.ui = UI()
        self.ui.calculate_offsets(self.state.board)

        self.stack = 1
        self.selected_tile = None
        self.selection = []

        self.mouse = Mouse()

    def save(self):
        with open("state.json", 'w') as file:
            data = json.dumps(dict(self.state), indent=4)
            file.write(data)

    def quit(self, save=True):
        if save:
            self.save()

        pygame.quit()
        sys.exit()

    def frame(self):
        wheel = 0
        for event in pygame.event.get():
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_r:
                    self.state = State()
                    self.ui.calculate_offsets(self.state.board)
                if event.key == locals.K_ESCAPE:
                    self.quit()
            if event.type == locals.QUIT:
                self.quit()
            elif event.type == locals.MOUSEWHEEL:
                wheel = event.y

        self.mouse.update(wheel=wheel)
        current_tile = self.ui.get_position(self.mouse.position())

        tiles_to_draw = []
        offset = 0
        if not self.state.end:
            if self.state.initial_phase:
                if current_tile in self.state.board:
                    tiles_to_draw.append((current_tile, (self.state.turn, self.state.stack_size if self.state.board.is_tile_boundary(current_tile) else 0), True))
                    if self.mouse.released():
                        self.state.place_initial_stack(current_tile)
            else:
                if self.selected_tile:
                    if self.selected_tile == current_tile:
                        if self.mouse.released():
                            self.selection = []
                            self.selected_tile = None
                            self.stack = 1
                    else:
                        self.stack = max(1, min(self.state.board(self.selected_tile).value - 1, self.stack + self.mouse.wheel()))
                        direction = self.ui.get_direction(self.selected_tile, current_tile)
                        tiles_in_direction = self.state.board.get_tiles_in_direction(self.selected_tile, direction)
                        if tiles_in_direction:
                            offset = -self.stack
                            ending_tile = tiles_in_direction[-1]
                            for tile in tiles_in_direction:
                                tiles_to_draw.append(
                                    (tile, Tile(self.state.turn, self.stack if tile == ending_tile else 0), True))

                            if self.mouse.released():
                                self.state.move(self.selected_tile, direction, size=self.stack)
                                self.selection = []
                                self.selected_tile = None
                                self.stack = 1
                else:
                    if current_tile in self.state.board:
                        if self.state.board(current_tile).player == 0:
                            tiles_to_draw.append((current_tile, Tile(self.state.turn, 0), True))
                            self.selection = [self.selected_tile]
                        elif self.state.board(current_tile).player == self.state.turn:
                            self.selection = [current_tile]
                    if self.state.get_possible_moves(current_tile) and self.state.board.is_tile_movable(current_tile):
                        if self.mouse.released():
                            self.selected_tile = current_tile
                            self.selection = [current_tile]

        self.ui.draw_board(self.state, selection=self.selection, offset=offset)
        for tile, pair, transparent in tiles_to_draw:
            self.ui.draw_tile(tile, pair, transparent=transparent)

        pygame.display.update()
        self.clock.tick(self.fps)


game = Game()
while True:
    try:
        game.frame()
    except KeyboardInterrupt:
        game.quit(save=False)
