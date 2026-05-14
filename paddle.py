import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    """Paddle class"""
    def __init__(self, game, groups, obstacles, pos=None, shrink=False, full_width=False):
        super().__init__(groups)
        self.build_paddle(pos, shrink=shrink, full_width=full_width)
        self.speed = PADDLE_SPEED
        self.direction = pygame.Vector2(0, 0)

        self.obstacles = obstacles
        self.game = game

        self.shrinked = False

    def update(self, dt):
        """Paddle update"""
        if not self.game.mode == 'ATTRACT':
            self.input()
            self.movement(dt)

    def build_paddle(self, pos=None, shrink=False, full_width=False):
        """Build new paddle"""
        if full_width: paddle_size = ((WIDTH - (2 * OFFSET_X) - (2 * WALL_THICKNESS)), PADDLE_HEIGHT)
        elif shrink: paddle_size = (int(PADDLE_WIDTH / 1.5), PADDLE_HEIGHT)
        else: paddle_size = (PADDLE_WIDTH, PADDLE_HEIGHT)

        paddle_pos = pos or (WIDTH // 2, HEIGHT - 20)

        self.image = pygame.Surface(paddle_size)
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect(midbottom = paddle_pos)

    def get_current_pos(self):
        """Get current position"""
        return self.rect.midbottom

    def input(self):
        """User input"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.direction.x = -1
        elif keys[pygame.K_RIGHT]: self.direction.x = 1
        else: self.direction = pygame.Vector2()

    def movement(self, dt):
        """Paddle movement"""
        if self.direction.x != 0:
            self.rect.x += self.direction.x * self.speed * dt

            # --- Check collision with walls ---
            hit_list = pygame.sprite.spritecollide(self, self.obstacles, False)

            for sprite in hit_list:
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right