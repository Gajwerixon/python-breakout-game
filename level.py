import pygame

from math import ceil
from settings import *

class Level:
    """Level class"""
    def __init__(self, surface, all_sprites, obstacles):
        self.all_sprites = all_sprites
        self.obstacles = obstacles
        self.surface = surface

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
                Brick(current_color, x, y, col_idx, groups)

    def reset(self):
        """Reset level"""
        for obstacle in self.obstacles:
            if getattr(obstacle, 'is_brick', False):
                obstacle.kill()
        
        self.create_bricks()

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
    def __init__(self, color, pos_x, pos_y, col_idx, groups):
        super().__init__(groups)
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        # --- Fill with black (for border) ---
        self.image.fill('black')

        # --- Add inner rect ---
        inner_rect = pygame.Rect(2, 2, BRICK_WIDTH - 4, BRICK_HEIGHT - 4)
        self.color = color
        pygame.draw.rect(self.image, self.color, inner_rect)
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

        self.score = self.get_score()
        self.is_brick = True

    def get_score(self):
        """Score assign"""
        if self.color == (231, 235, 12): return 1
        elif self.color == (12, 235, 45): return 3
        elif self.color == (232, 132, 9): return 5
        else: return 7