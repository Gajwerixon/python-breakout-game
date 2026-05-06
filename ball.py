import pygame
import math

from settings import *
from random import randint, uniform, choice

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, paddle):
        super().__init__(groups)
        self.obstacles = obstacles
        self.paddle = paddle

        self.image = pygame.Surface((BALL_WIDTH, BALL_HEIGHT))
        self.image.fill(BALL_COLOR)

        self.rect = self.image.get_rect(center = self.get_ball_start_pos())
        self.pos = pygame.Vector2(self.rect.center)

        self.speed = BALL_START_SPEED
        self.direction = self.get_ball_start_direction().normalize()

    def get_ball_start_pos(self):
        """Choose random ball start position"""
        pos_y = BALL_START_Y
        pos_x = 300
        return (pos_x, pos_y)
    
    def get_ball_start_direction(self):
        """Select random ball start direction"""
        x = 0.5
        y = 0.5
        return pygame.Vector2(x, y)
    
    def movement(self, dt):
        """Ball movement"""
        # --- Horizontal ---
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        self.collision('horizontal')

        # --- Vertical ---
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
        self.collision('vertical')

    def collision(self, axis):
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
        """
        Coordinates ball behavior upon collision with the paddle.
        Separates horizontal (side) and vertical (top) bounce logic.
        """
        if axis == 'horizontal':
            self._handle_side_collision()
        else:
            self._handle_top_collision()

        # --- Synchronize logical position with physical rect ---
        self.pos = pygame.Vector2(self.rect.center)

    def _handle_side_collision(self):
        """Handles ball hitting the left or right side of the paddle."""
        if self.rect.centerx < self.paddle.rect.centerx: 
            self.rect.right = self.paddle.rect.left - 5
            self.direction.x = -abs(self.direction.x)
        else: 
            self.rect.left = self.paddle.rect.right + 5
            self.direction.x = abs(self.direction.x)
        
        # --- Ensure clean bounce by resolving paddle-ball intersection ---
        self.speed = self.speed + (self.paddle.speed * 0.2)
        
    def _handle_top_collision(self):
        """Handles ball bouncing off the top surface of the paddle."""
        self.rect.bottom = self.paddle.rect.top

        # --- Calculate hit position relative to center (-1.0 to 1.0) ---
        half_width = PADDLE_WIDTH / 2
        influence = (self.rect.centerx - self.paddle.rect.centerx) / half_width
        
        # --- Ensure a minimum horizontal kick for center hits ---
        if abs(influence) < 0.2:
            influence = math.copysign(0.2, influence)

        # --- Apply influence and flip vertical direction ---
        self.direction.x = influence * 1.25
        self.direction.y *= -1

        # --- Prevent the ball from traveling too horizontally ---
        if abs(self.direction.y) < 0.3:
            self.direction.y = math.copysign(0.3, self.direction.y)

        # --- Final normalization to keep speed consistent ---
        self.direction = self.direction.normalize()

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

        # --- If the ball hit between two bricks kill them all ---
        for hit in hits:
            if getattr(hit, 'is_brick', False):
                hit.kill()
        
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt):
        """Update ball"""
        self.movement(dt)    