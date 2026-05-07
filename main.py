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
        self.game_active = False
        
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

    def run_game(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # --- Update game ---
            self.update_game(dt)

            # --- Draw and refresh screen ---
            self.draw_screen()
        
        # --- Quit game ---
        pygame.quit()
        exit()

    def update_game(self, dt):
        """Update game"""
        self.all_sprites.update(dt)

    def draw_screen(self):
        """Draw on screen"""
        self.surface.fill('black')

        self.all_sprites.draw(self.surface)

        self.ui.show_score(self.level.score)

        pygame.display.flip()
    
game = Game()
game.run_game()