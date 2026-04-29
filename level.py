import pygame
from settings import *

class Level:
    """Level class"""
    def __init__(self, groups):
        self.groups = groups

    def create_walls(self):
        """Create walls"""
        top = Wall(WIDTH - OFFSET_X * 2, WALL_THICKNESS, OFFSET_X, OFFSET_Y, self.groups)
        left = Wall(WALL_THICKNESS, HEIGHT, OFFSET_X, 0, self.groups)
        right = Wall(WALL_THICKNESS, HEIGHT, WIDTH - OFFSET_X, 0,  self.groups)

class Wall(pygame.sprite.Sprite):
    """Wall class"""
    def __init__(self, width, height, pos_x, pos_y, groups):
        super().__init__(groups)
        self.image = pygame.Surface((width, height))
        self.image.fill(WALL_COLOR)

        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

class Brick(pygame.sprite.Sprite):
    """Brick class"""
    def __init__(self, groups):
        super().__init__(groups)