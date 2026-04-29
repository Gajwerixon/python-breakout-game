import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # --- Paddle image ---
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(PADDLE_COLOR)

        # --- Paddle rect ---
        self.rect = self.image.get_rect(midbottom = (WIDTH // 2, HEIGHT - 20))

        # --- Paddle movement ---
        self.speed = PADDLE_SPEED
        self.direction = pygame.Vector2(0, 0)

    def input(self):
        """User input"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.direction = pygame.Vector2(1, 0)
        else:
            self.direction = (0, 0)

    def movement(self, dt):
        """Paddle movement"""
        self.rect.x += self.direction[0] * self.speed * dt

    def update(self, dt):
        """Paddle update"""
        self.input()
        self.movement(dt)

    