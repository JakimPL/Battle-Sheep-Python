from board import Tile
from mouse import Mouse
from state import State
from ui import UI
import json
import pygame
import sys
from pygame import locals


pygame.init()
clock = pygame.time.Clock()
FPS = 60

state = State()
ui = UI()
ui.calculate_offsets(state.board)

stack = 1
selected_tile = None
selection = []

mouse = Mouse()
while True:
    wheel = 0
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            with open("state.json", 'w') as file:
                json.dump(dict(state), file, indent=4)
            pygame.quit()
            sys.exit()
        elif event.type == locals.MOUSEWHEEL:
            wheel = event.y

    mouse.update(wheel=wheel)
    current_tile = ui.get_position(mouse.position())

    tiles_to_draw = []
    offset = 0
    if not state.end:
        if state.initial_phase:
            if current_tile in state.board:
                tiles_to_draw.append((current_tile, (state.turn, state.stack_size if state.board.is_tile_boundary(current_tile) else 0), True))
                if mouse.released():
                    state.place_initial_stack(current_tile)
        else:
            if selected_tile:
                if selected_tile == current_tile:
                    if mouse.released():
                        selection = []
                        selected_tile = None
                        stack = 1
                else:
                    stack = max(1, min(state.board(selected_tile).value - 1, stack + mouse.wheel()))
                    direction = ui.get_direction(selected_tile, current_tile)
                    tiles_in_direction = state.board.get_tiles_in_direction(selected_tile, direction)
                    if tiles_in_direction:
                        offset = -stack
                        value = state.board(selected_tile).value
                        ending_tile = tiles_in_direction[-1]
                        for tile in tiles_in_direction:
                            tiles_to_draw.append((tile, Tile(state.turn, stack if tile == ending_tile else 0), True))

                        if mouse.released():
                            state.move(selected_tile, direction, size=stack)
                            selection = []
                            selected_tile = None
                            stack = 1
            else:
                if current_tile in state.board:
                    if state.board(current_tile).player == 0:
                        tiles_to_draw.append((current_tile, Tile(state.turn, 0), True))
                        selection = [selected_tile]
                    elif state.board(current_tile).player == state.turn:
                        selection = [current_tile]
                if state.get_possible_moves(current_tile) and state.board.is_tile_movable(current_tile):
                    if mouse.released():
                        selected_tile = current_tile
                        selection = [current_tile]

    ui.draw_board(state, selection=selection, offset=offset)
    for tile, pair, transparent in tiles_to_draw:
        ui.draw_tile(tile, pair, transparent=transparent)

    pygame.display.update()
    clock.tick(FPS)
