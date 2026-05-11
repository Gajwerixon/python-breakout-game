import pygame
from settings import *
from sys import exit

from paddle import Paddle
from ball import Ball
from level import Level
from ui import UI

class Game:
    """Main game class"""
    def __init__(self):
        # --- Basic setup ---   
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Breakout')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = True

        # --- Game variables ---
        self.lives = 1
        self.current_level = 1
        self.high_score = 0
        self.score = 0
        self.hits = 0

        # --- Timers ---
        self.round_reset_timer = None
        self.game_reset_timer = None
        
        # --- Sprites ---
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.level = Level(self.surface, self.all_sprites, self.obstacles)
        self.paddle = Paddle(self.all_sprites, self.obstacles)
        self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)

        # --- Initialize game ---
        self.level.initialize_game()
        self.ui = UI(self.surface)

    def run_game(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        """Handle basic events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()

    def update(self, dt):
        """Update game"""
        self.handle_ball_loss()

        self.handle_timers()
        
        if self.ball:
            self.update_difficulty()

        self.all_sprites.update(dt)

    def handle_ball_loss(self):
        """Handle if ball goes under screen"""
        if not self.ball:
            return

        if self.ball.rect.top <= HEIGHT:
            return

        self.lives += 1

        self.ball.kill()
        self.ball = None

        current_time = pygame.time.get_ticks()
        if self.lives < 4:
            self.round_reset_timer = current_time
        else:
            self.game_reset_timer = current_time

    def update_difficulty(self):
        """Update difficulty base on two conditions"""
        self.handle_speed_progression()
        if self.ball.is_above_bricks():
            self.paddle.shrink()

    def handle_speed_progression(self):
        """Handle speed progression base on hits and current score"""
        if self.hits in (4, 10, 20):
            self.ball.increase_speed(self.score)
            self.ball.speed_up = False
        else:        
            self.ball.speed_up = True

    def handle_timers(self):
        """Handle timers"""
        # --- Reset round ---
        if self.round_reset_timer:
            if pygame.time.get_ticks() - self.round_reset_timer > RESET_TIME_ROUNDS:
                self.reset_round()
                self.round_reset_timer = None
        
        # --- Reset game ---
        if self.game_reset_timer:
            self.game_active = False
            if pygame.time.get_ticks() - self.game_reset_timer > RESET_TIME_GAME:
                self.reset_game()
                self.game_reset_timer = None

    def reset_round(self):
        """Reset round"""
        self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)
        self.ball.speed = BALL_START_SPEED
        self.ball.speed_up = 0

        if self.paddle.shrinked:
            old_pos = self.paddle.get_current_pos()
            self.paddle.kill()
            self.paddle = Paddle(self.all_sprites, self.obstacles, old_pos)
            self.paddle.shrinked = False

        self.hits = 0
        self.round_reset_timer = None

    def reset_game(self):
        """Reset game after player loss all 3 lives"""
        self.paddle.kill()

        self.level.reset()

        self.paddle = Paddle(self.all_sprites, self.obstacles)
        self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)

        self.current_level = 1
        self.lives = 1
        self.score = 0
        
        self.hits = 0

        self.save_high_score()

        self.game_active = True

    def draw(self):
        """Draw on screen"""
        self.surface.fill('black')

        self.all_sprites.draw(self.surface)

        self.ui.show_ui(
            self.current_level, 
            self.score, 
            self.lives, 
            self.high_score, 
            self.game_active
        )

        pygame.display.flip()

    def save_high_score(self):
        """Save high score"""
        pass

game = Game()
game.run_game()