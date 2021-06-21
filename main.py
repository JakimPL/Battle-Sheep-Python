from state import State
from ui import UI
import pygame
import sys
from pygame import locals

pygame.init()
clock = pygame.time.Clock()
FPS = 60

state = State(4)
ui = UI()
ui.calculate_offsets(state.board)
while True:
    ui.draw_board(state)
    current_tile = ui.get_position(pygame.mouse.get_pos())
    if state.initial_phase:
        if current_tile in state.board:
            ui.draw_tile(current_tile, (state.turn, state.stack_size))
            if pygame.mouse.get_pressed(3)[0]:
                state.place_initial_stack(current_tile)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
