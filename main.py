from state import State
from ui import UI
import pygame
import sys
from pygame import locals

pygame.init()
state = State(4)
ui = UI()
ui.calculate_offsets(state.board)
while True:
    ui.draw_board(state)
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            pygame.quit()
            sys.exit()
