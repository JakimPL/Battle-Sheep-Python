import pygame
from state import State
from config import Config


class UI:
    def __init__(self):
        config = Config()
        self.line = 0
        self.tile_size = 60

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

        self.font_size = 14
        self.font = pygame.font.SysFont(config.font, self.font_size)
        self.display = pygame.display.set_mode((self.game_width, self.game_height), 0, 32)

    def calculate_offsets(self, board):
        min_x, min_y, max_x, max_y = None, None, None, None
        for tile in board:
            x, y = tile
            _x, _y = x * 0.84 * self.tile_size, (y + 0.5 * x) * self.tile_size
            if (min_x is None) or _x < min_x:
                min_x = _x
            if (max_x is None) or _x > max_x:
                max_x = _x
            if (min_y is None) or _y < min_y:
                min_y = _y
            if (max_y is None) or _y > max_y:
                max_y = _y

        if not (min_x is None or max_x is None):
            self.x_offset = (self.game_width - (max_x - min_x)) / 2

        if not (min_y is None or max_y is None):
            self.y_offset = (self.game_height - (max_y - min_y)) / 2

    def draw_board(self, state: State):
        pygame.draw.rect(self.display, self.colors[state.turn], (0, 0, self.game_width, self.game_height))

        for tile in state.board:
            x, y = tile
            _x, _y = x * 0.84 * self.tile_size - self.new_rect[0] / 2, (y + 0.5 * x) * self.tile_size - self.new_rect[1] / 2
            self.display.blit(self.sprites[state.board(tile)], (_x + self.x_offset, _y + self.y_offset))

        pygame.display.update()
