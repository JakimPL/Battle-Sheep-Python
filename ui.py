import pygame
from state import State
from config import Config


class UI:
    def __init__(self):
        config = Config()
        self.line = 0
        self.tile_size = 35

        self.game_width = 800
        self.game_height = 600
        self.x_offset = 0
        self.y_offset = 0

        self.sprite = pygame.image.load("hex.png")
        self.rect = self.sprite.get_rect()[2:]
        self.scale = self.tile_size / self.rect[1]
        self.new_rect = (int(self.rect[0] * self.scale), int(self.rect[1] * self.scale))
        self.sprites = [pygame.image.load("hex_{0}.png".format(i)) for i in range(5)]
        for i in range(5):
            self.sprites[i] = pygame.transform.scale(self.sprites[i], self.new_rect)

        self.colors = [(64, 160, 64), (224, 224, 224), (32, 32, 32), (224, 64, 64), (64, 64, 224)]
        self.comp_colors = [(32, 32, 32), (16, 16, 16), (224, 224, 224), (224, 224, 224), (224, 224, 224)]

        self.font_size = 14
        self.font = pygame.font.SysFont(config.font, self.font_size)
        self.display = pygame.display.set_mode((self.game_width, self.game_height), 0, 32)

    def get_position(self, pos):
        x, y = pos[0] - self.x_offset, pos[1] - self.y_offset
        return round((50 * x) / (42 * self.tile_size)), round((84 * y - 50 * x) / (84 * self.tile_size))

    def get_real_position(self, tile):
        x, y = tile
        return self.x_offset + x * 0.84 * self.tile_size - self.new_rect[0] / 2, \
            self.y_offset + (y + 0.50 * x) * self.tile_size - self.new_rect[1] / 2

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

    def draw_board(self, state: State):
        pygame.draw.rect(self.display, self.colors[state.turn], (0, 0, self.game_width, self.game_height))

        for tile in state.board:
            self.draw_tile(tile, state.board(tile))

    def draw_tile(self, tile, pair):
        x, y = self.get_real_position(tile)
        player, quantity = pair
        self.display.blit(self.sprites[player], (x, y))

        if quantity > 0:
            label = self.font.render(str(quantity), True, self.comp_colors[player])
            w, h = label.get_rect()[2:]
            self.display.blit(label, (x + (self.new_rect[0] - w) / 2, y + (self.new_rect[1] - h) / 2))
