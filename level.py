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

        Wall(WIDTH - OFFSET_X * 2, WALL_THICKNESS, OFFSET_X, OFFSET_Y, (self.obstacles, self.all_sprites))
        Wall(WALL_THICKNESS, HEIGHT, OFFSET_X, 0, (self.obstacles, self.all_sprites))
        Wall(WALL_THICKNESS, HEIGHT, WIDTH - OFFSET_X, 0, groups)

    def create_bricks(self):
        """Create bricks"""
        groups = (self.all_sprites, self.obstacles)

        for col_idx in range(BRICK_COLS):
            color_idx = (col_idx // ROWS_PER_COLOR) % len(BRICK_COLORS)
            current_color = BRICK_COLORS[color_idx]
            for row in range(BRICKS_ROW):
                x = MARGIN_X + BRICK_WIDTH * row
                y = MARGIN_Y + BRICK_HEIGHT * (col_idx)
                Brick(current_color, x, y, groups)

class Wall(pygame.sprite.Sprite):
    """Wall class"""
    def __init__(self, width, height, pos_x, pos_y, groups):
        super().__init__(groups)
        self.image = pygame.Surface((width, height))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

        self.is_wall = True

class Brick(pygame.sprite.Sprite):
    """Brick class"""
    def __init__(self, color, pos_x, pos_y, groups):
        super().__init__(groups)
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        # --- Fill with black (for border) ---
        self.image.fill('black')

        # --- Add inner rect ---
        inner_rect = pygame.Rect(2, 2, BRICK_WIDTH - 4, BRICK_HEIGHT - 4)
        pygame.draw.rect(self.image, color, inner_rect)
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

        self.is_brick = True