from board import Tile
from mouse import Mouse
from state import State
from ui import UI
import pygame
import sys
from pygame import locals


pygame.init()
clock = pygame.time.Clock()
FPS = 60

state = State()
ui = UI()
ui.calculate_offsets(state.board)
selected_tile = None
selection = []

mouse = Mouse()
while True:
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            pygame.quit()
            sys.exit()

    mouse.update(pygame.mouse.get_pressed(3)[0])
    #print(mouse.pressed(), mouse.released())
    ui.draw_board(state, selection=selection)
    current_tile = ui.get_position(pygame.mouse.get_pos())
    if not state.end:
        if state.initial_phase:
            if current_tile in state.board:
                ui.draw_tile(current_tile,
                             (state.turn, state.stack_size if state.board.is_tile_boundary(current_tile) else 0),
                             transparent=True)
                if mouse.released():
                    state.place_initial_stack(current_tile)
        else:
            if selected_tile:
                if selected_tile == current_tile:
                    if mouse.released():
                        selection = []
                        selected_tile = None
                else:
                    direction = ui.get_direction(selected_tile, current_tile)
                    tiles_in_direction = state.board.get_tiles_in_direction(selected_tile, direction)
                    if tiles_in_direction:
                        value = state.board(selected_tile).value
                        for tile in tiles_in_direction:
                            ui.draw_tile(tile, Tile(state.turn, 0), transparent=True)

                        if mouse.pressed():
                            state.move(selected_tile, direction)
                            selection = []
                            selected_tile = None
            else:
                if current_tile in state.board:
                    if state.board(current_tile).player == 0:
                        ui.draw_tile(current_tile, Tile(state.turn, 0), transparent=True)
                        selection = [selected_tile]
                    elif state.board(current_tile).player == state.turn:
                        selection = [current_tile]
                if state.get_possible_moves(current_tile) and state.board.is_tile_movable(current_tile):
                    if mouse.released():
                        selected_tile = current_tile
                        selection = [current_tile]

    pygame.display.update()

    clock.tick(FPS)
