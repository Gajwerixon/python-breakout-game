import pygame

from settings import *
from random import randint, uniform, choice

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, paddle):
        super().__init__(groups)
        self.obstacles = obstacles
        self.paddle = paddle

        self.image = pygame.Surface((BALL_WIDTH, BALL_HEIGHT))
        self.image.fill(BALL_COLOR)

        self.rect = self.image.get_rect(center = self.ball_start_pos)
        self.pos = pygame.Vector2(self.rect.center)

        self.speed = BALL_START_SPEED
        self.direction = self.ball_start_direction.normalize()

    @property
    def ball_start_pos(self):
        """Choose random ball start position"""
        pos_y = BALL_START_Y
        pos_x = randint(350, 450)
        return (pos_x, pos_y)
    
    @property
    def ball_start_direction(self):
        """Select random ball start direction"""
        x = uniform(0.475, 0.525) * choice([-1, 1])
        y = uniform(0.475, 0.525)
        return pygame.Vector2(x, y)
    
    def movement(self, dt):
        """Ball movement"""
        # --- Horizontal ---
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        self.collsion('horizontal')

        # --- Vertical ---
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
        self.collsion('vertical')

    def collsion(self, axis):
        """Detect collision"""
        # --- Collision with paddle ---
        if pygame.sprite.collide_rect(self, self.paddle):
            self.handle_paddle_collision(axis)
            return
        
        # --- Collision with obstacles ---
        hits = pygame.sprite.spritecollide(self, self.obstacles, False)
        if hits:
            self.handle_obstacle_collision(hits, axis)
    
    def handle_paddle_collision(self, axis):
        """Handle collision with paddle"""
        # --- Horizontal ---
        if axis == 'horizontal':
            if self.rect.centerx < self.paddle.rect.centerx: 
                self.rect.right = self.paddle.rect.left - 5
                self.direction.x = -abs(self.direction.x)
            else: 
                self.rect.left = self.paddle.rect.right + 5
                self.direction.x = abs(self.direction.x)
            self.speed = self.paddle.speed
        
        # --- Vertical ---
        else:
            self.rect.bottom = self.paddle.rect.top
            influence = (self.rect.centerx - self.paddle.rect.centerx) / (PADDLE_WIDTH / 2)
            self.direction.x += influence * 0.5
            self.direction.y *= -1
            self.direction = self.direction.normalize()

        print(self.direction)
        self.pos = pygame.Vector2(self.rect.center)

    def handle_obstacle_collision(self, hits, axis):
        """Handle collision with obstacles (walls and bricks)"""
        obstacle = hits[0]
        if axis == 'horizontal':
            if self.direction.x > 0: self.rect.right = obstacle.rect.left
            else: self.rect.left = obstacle.rect.right
            self.direction.x *= -1
        else:
            if self.direction.y > 0:
                self.rect.bottom = obstacle.rect.top
            else:
                self.rect.top = obstacle.rect.bottom
            self.direction.y *= -1

        if getattr(obstacle, 'is_brick', False):
            obstacle.kill()
        
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt):
        """Update ball"""
        self.movement(dt)    