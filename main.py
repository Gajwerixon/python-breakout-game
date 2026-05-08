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
        
        # --- Sprites ---
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.level = Level(self.surface, self.all_sprites, self.obstacles)
        self.paddle = Paddle(self.all_sprites, self.obstacles)
        self.ball = Ball(self.level, self.paddle, self.all_sprites, self.obstacles)

        # --- Initialize game ---
        self.level.initialize_game()

        # --- User Interface---
        self.ui = UI(self.surface)

        # --- Game variables ---
        self.lives = 2
        self.current_level = 1
        self.high_score = 0

        # --- Time ---
        self.round_reset_timer = None
        self.game_reset_timer = None

    def run_game(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.round_reset_timer and not self.game_reset_timer:
                if self.check_dead():
                    self.lives -= 1
                    if self.lives >= 0:
                        self.round_reset_timer = self.current_time()
                    elif self.lives < 0:
                        self.game_reset_timer = self.current_time()
                    self.ball.kill()
            
            if self.round_reset_timer:
                if pygame.time.get_ticks() - self.round_reset_timer > RESET_TIME_ROUNDS:
                    self.ball = Ball(self.level, self.paddle, self.all_sprites, self.obstacles)
                    self.round_reset_timer = None
            
            if self.game_reset_timer:
                if pygame.time.get_ticks() - self.game_reset_timer > RESET_TIME_GAME:
                    self.reset_game()
                    self.game_reset_timer = None

            self.update_game(dt)
            self.draw_screen()
        
        # --- Quit game ---
        pygame.quit()
        exit()

    def update_game(self, dt):
        """Update game"""
        self.all_sprites.update(dt)

    def check_dead(self):
        """Check ball dead"""
        if self.ball.rect.top >= HEIGHT:
            return True
        return False

    def reset_game(self):
        """Reset game after player loss all 3 lives"""
        # --- Kill old sprites ---
        self.paddle.kill()

        # --- Reset game ---
        self.level.reset()

        # --- Create new sprites ---
        self.paddle = Paddle(self.all_sprites, self.obstacles)
        self.ball = Ball(self.level, self.paddle, self.all_sprites, self.obstacles)

        # --- Reset game stats ---
        self.current_level = 1
        self.lives = 2

        # --- Save high score (if occur) ---
        self.save_high_score()

    def draw_screen(self):
        """Draw on screen"""
        self.surface.fill('black')

        self.all_sprites.draw(self.surface)

        self.ui.show_ui(self.current_level, self.level.score, 
                        self.lives, self.high_score)

        pygame.display.flip()

    def save_high_score(self):
        pass
    
    def current_time(self):
        return pygame.time.get_ticks()

game = Game()
game.run_game()