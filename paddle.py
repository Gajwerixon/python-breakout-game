import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles):
        super().__init__(groups)
        # --- Paddle image ---
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(PADDLE_COLOR)

        # --- Paddle rect ---
        self.rect = self.image.get_rect(midbottom = (WIDTH // 2, HEIGHT - 20))

        # --- Paddle movement ---
        self.speed = PADDLE_SPEED
        self.direction = pygame.Vector2(0, 0)

        # --- Obstacles -> walls ---
        self.obstacles = obstacles

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
        if self.direction != 0:
            self.rect.x += self.direction[0] * self.speed * dt

            hit_list = pygame.sprite.spritecollide(self, self.obstacles, False)

            for sprite in hit_list:
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right

    def update(self, dt):
        """Paddle update"""
        self.input()
        self.movement(dt)

    