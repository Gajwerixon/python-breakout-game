import pygame

from settings import *

class UI:
    """User Interface class"""
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font('assets/Emulogic.ttf', FONT_SIZE)

    def show_ui(self, level, score, lives, high_score):
        self.show_current_level(level)
        self.show_score(score)
        self.show_lives(lives)
        self.show_high_score(high_score)

    def show_current_level(self, level):
        """Show current level on screen"""
        text_surface = self.font.render(f'{level}', True, 'white')
        text_rect = text_surface.get_rect(topleft=(LEVEL_POS_X, LEVEL_POS_Y))

        self.surface.blit(text_surface, text_rect)

    def show_score(self, score):
        """Show score on screen"""
        text_surface = self.font.render(f'{score:03d}', True, 'white')
        text_rect = text_surface.get_rect(topright = (SCORE_POS_X, SCORE_POS_Y))

        self.surface.blit(text_surface, text_rect)

    def show_lives(self, lives):
        """Show player lives on screen"""
        if lives < 0:
            lives = 0
        text_surface = self.font.render(f'{lives}', True, 'white')
        text_rect = text_surface.get_rect(topleft=(LIVES_POS_X, LIVES_POS_Y))

        self.surface.blit(text_surface, text_rect)

    def show_high_score(self, high_score):
        """Show high score on screen"""
        text_surface = self.font.render(f'{high_score:03d}', True, 'white')
        text_rect = text_surface.get_rect(topright = (HIGH_SCORE_POS_X, HIGH_SCORE_POS_Y))

        self.surface.blit(text_surface, text_rect)
