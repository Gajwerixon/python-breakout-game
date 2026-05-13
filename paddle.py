import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    """Paddle class"""
    def __init__(self, groups, obstacles, pos=None, full_width=False):
        super().__init__(groups)
        self.build_paddle(pos, full_width=full_width)
        self.speed = PADDLE_SPEED
        self.direction = pygame.Vector2(0, 0)

        # --- Obstacles -> walls ---
        self.obstacles = obstacles

        # --- Shrink ---
        self.shrinked = False

        self.active = True

    def build_paddle(self, pos=None, shrink=False, full_width=False):
        """Build new paddle"""
        if full_width: 
            paddle_size = ((WIDTH - (2 * OFFSET_X) - (2 * WALL_THICKNESS)), PADDLE_HEIGHT)
        elif shrink: 
            paddle_size = (PADDLE_WIDTH / 2, PADDLE_HEIGHT)
        else: 
            paddle_size = (PADDLE_WIDTH, PADDLE_HEIGHT)

        if pos is None: paddle_pos = (WIDTH // 2, HEIGHT - 20)
        else: paddle_pos = (pos)

        self.image = pygame.Surface(paddle_size)
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect(midbottom = paddle_pos)

    def get_current_pos(self):
        """Get current position"""
        return self.rect.midbottom

    def shrink(self):
        """Shrink paddle"""
        if not self.shrinked:
            current_pos = self.get_current_pos()
            self.build_paddle(current_pos, True)
            self.shrinked = True

    def input(self):
        """User input"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]: self.direction = pygame.Vector2(1, 0)
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

    def update(self, dt):
        """Paddle update"""
        if self.active:
            self.input()
            self.movement(dt)

    