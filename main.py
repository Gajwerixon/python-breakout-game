import pygame
from settings import *
from sys import exit

# pygame setup
class Game:
    """Main game class"""
    def __init__(self):
        # --- Basic setup ---   
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = False

    def run_game(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # --- Draw and Refresh screen ---
            self.screen.fill('black')
            pygame.display.flip()
        
        # --- Quit game ---
        pygame.quit()
        exit()
    
game = Game()
game.run_game()