import math
import pygame
from board import DIRECTIONS
from config import Config
from state import State
from tile import Tile


class UI:
    def __init__(self):
        config = Config('ui')
        self.tile_size = config['tile_size']
        self.game_width, self.game_height = config['window_size']

        self.x_offset = 0
        self.y_offset = 0

        self.sprite = pygame.image.load("hex.png")
        self.rect = self.sprite.get_rect()[2:]
        self.scale = self.tile_size / self.rect[1]
        self.new_rect = (int(self.rect[0] * self.scale), int(self.rect[1] * self.scale))
        self.sprite = pygame.transform.scale(self.sprite, self.new_rect)

        self.colors = config['colors']
        self.comp_colors = config['comp_colors']
        self.turn_colors = config['turn_colors']

        self.sprites = []
        self.transparent_sprites = []
        for i in range(7):
            surface = pygame.Surface(self.sprite.get_size())
            surface.fill(self.colors[i])
            sprite = self.sprite.copy()
            sprite.blit(surface, (0, 0), special_flags=pygame.BLEND_MULT)
            transparent_sprite = sprite.copy()
            transparent_sprite.set_alpha(128)
            self.sprites.append(sprite)
            self.transparent_sprites.append(transparent_sprite)

        self.font_size = config['font_size']
        self.font = pygame.font.SysFont(config['font'], self.font_size)
        self.display = pygame.display.set_mode((self.game_width, self.game_height), 0, 32)

    def get_position(self, position):
        x, y = position[0] - self.x_offset, position[1] - self.y_offset
        return round((50 * x) / (42 * self.tile_size)), round((84 * y - 50 * x) / (84 * self.tile_size))

    def get_real_position(self, tile):
        x, y = tile
        return self.x_offset + x * 0.84 * self.tile_size - self.new_rect[0] / 2, \
            self.y_offset + (y + 0.50 * x) * self.tile_size - self.new_rect[1] / 2

    def get_direction(self, starting_position, ending_position):
        x1, y1 = self.get_real_position(starting_position)
        x2, y2 = self.get_real_position(ending_position)
        angle = round(3 / math.pi * math.atan2(y2 - y1, x2 - x1) + 6.5) % 6
        return DIRECTIONS[angle]

    def calculate_offsets(self, board):
        xs = []
        ys = []
        for tile in board:
            x, y = tile
            xs.append(x * 0.84 * self.tile_size)
            ys.append((y + 0.5 * x) * self.tile_size)

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        self.x_offset = (self.game_width - (max_x - min_x)) / 2 - min_x
        self.y_offset = (self.game_height - (max_y - min_y)) / 2 - min_y

    def draw_board(self, state: State, selection=None, offset=0):
        pygame.draw.rect(self.display, self.turn_colors[state.turn], (0, 0, self.game_width, self.game_height))

        for tile in state.board:
            if tile in selection:
                player, value = state.board(tile)
                self.draw_tile(tile, Tile(0, 0))
                self.draw_tile(tile, Tile(player, value + offset), transparent=True)
            else:
                self.draw_tile(tile, state.board(tile))

    def draw_tile(self, tile, pair, transparent=False):
        x, y = self.get_real_position(tile)
        player, quantity = pair
        self.display.blit(self.transparent_sprites[player] if transparent else self.sprites[player], (x, y))

        if quantity > 0:
            label = self.font.render(str(quantity), True, self.comp_colors[player])
            w, h = label.get_rect()[2:]
            self.display.blit(label, (x + (self.new_rect[0] - w) / 2, y + (self.new_rect[1] - h) / 2))
