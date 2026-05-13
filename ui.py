import pygame

from settings import *

class UI:
    """User Interface class"""
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font('assets/Emulogic.ttf', FONT_SIZE)

        self.score_status = 'show'
        self.current_time = 0

        self.level_up = False
        self.level_status = 'show'

    def show_ui(self, level, score, lives, high_score, game_status):
        if not self.level_up:
            self.update_score_visibility(score, game_status)
            self.show_current_level(level)
            self.show_lives(lives)
            self.show_high_score(high_score)
        if self.level_up:
            if self.level_status == 'show':
                self.show_current_score(score)
                self.show_current_level(level)
                self.show_lives(lives)
                self.show_high_score(high_score)
                if pygame.time.get_ticks() - self.current_time >= LEVEL_UP_BLIT:
                    self.level_status = 'hide'
                    self.current_time = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.current_time >= LEVEL_UP_HIDE:
                    self.level_status = 'show'
                    self.current_time = pygame.time.get_ticks()

    def update_score_visibility(self, score, game_status):
        """Update score visibility"""
        if game_status == True:
            if self.score_status == 'show':
                self.show_current_score(score)
                if pygame.time.get_ticks() - self.current_time >= SCORE_BLIT:
                    self.score_status = 'hide'
                    self.current_time = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.current_time >= SCORE_HIDE:
                    self.score_status = 'show'
                    self.current_time = pygame.time.get_ticks()
        else:
            self.show_current_score(score)
            self.score_status = 'show'

    def show_current_score(self, score):
        """Show score on screen"""
        text_surface = self.font.render(f'{score:03d}', True, 'white')
        text_rect = text_surface.get_rect(topright = (SCORE_POS_X, SCORE_POS_Y))

        self.surface.blit(text_surface, text_rect)

    def show_current_level(self, level):
        """Show current level on screen"""
        text_surface = self.font.render(f'{level}', True, 'white')
        text_rect = text_surface.get_rect(topleft=(LEVEL_POS_X, LEVEL_POS_Y))

        self.surface.blit(text_surface, text_rect)

    def show_lives(self, lives):
        """Show player lives on screen"""
        text_surface = self.font.render(f'{lives}', True, 'white')
        text_rect = text_surface.get_rect(topleft=(LIVES_POS_X, LIVES_POS_Y))

        self.surface.blit(text_surface, text_rect)

    def show_high_score(self, high_score):
        """Show high score on screen"""
        text_surface = self.font.render(f'{high_score:03d}', True, 'white')
        text_rect = text_surface.get_rect(topright = (HIGH_SCORE_POS_X, HIGH_SCORE_POS_Y))

        self.surface.blit(text_surface, text_rect)
