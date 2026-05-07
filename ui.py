import pygame

from settings import *

class UI:
    """User Interface class"""
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font('assets/Emulogic.ttf', 28)

    def show_score(self, score):
        """Show score on screen"""
        text_surface = self.font.render(f'{score}', True, 'white')
        text_rect = text_surface.get_rect(topleft = (SCORE_POS_X, SCORE_POS_Y))

        self.surface.blit(text_surface, text_rect)