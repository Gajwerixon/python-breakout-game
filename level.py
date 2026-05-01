import pygame
from settings import *

class Level:
    """Level class"""
    def __init__(self, all_sprites, obstacles):
        self.all_sprites = all_sprites
        self.obstacles = obstacles

    def initialize_game(self):
        """Initialize game"""
        self.create_walls()
        self.create_bricks()

    def create_walls(self):
        """Create walls"""
        groups = (self.all_sprites, self.obstacles)

        top = Wall(WIDTH - OFFSET_X * 2, WALL_THICKNESS, OFFSET_X, OFFSET_Y, (self.obstacles, self.all_sprites))
        left = Wall(WALL_THICKNESS, HEIGHT, OFFSET_X, 0, (self.obstacles, self.all_sprites))
        right = Wall(WALL_THICKNESS, HEIGHT, WIDTH - OFFSET_X, 0, groups)

    def create_bricks(self):
        """Create bricks"""
        groups = (self.all_sprites, self.obstacles)

        for col_idx in range(BRICK_COLS):
            color_idx = (col_idx // ROWS_PER_COLOR) % len(BRICK_COLORS)
            current_color = BRICK_COLORS[color_idx]
            for row in range(BRICKS_ROW):
                x = MARGIN_X + (BRICK_GAP + BRICK_WIDTH) * row
                y = MARGIN_Y + (BRICK_HEIGHT + BRICK_GAP) * (col_idx)
                Brick(current_color, x, y, groups)

class Wall(pygame.sprite.Sprite):
    """Wall class"""
    def __init__(self, width, height, pos_x, pos_y, groups):
        super().__init__(groups)
        self.image = pygame.Surface((width, height))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

class Brick(pygame.sprite.Sprite):
    """Brick class"""
    def __init__(self, color, pos_x, pos_y, groups):
        super().__init__(groups)
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
