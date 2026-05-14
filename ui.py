import pygame

from settings import *

class UI:
    """User Interface class"""
    def __init__(self, game):
        self.game = game
        self.surface = game.surface

        self.font = pygame.font.Font('assets/Emulogic.ttf', FONT_SIZE)

        self.timers = {'score': 0, 'level': 0}
        self.level_status = 'show'
        self.score_status = 'show'

    def draw(self):
        """Draw ui"""
        if self.game.mode == 'PLAYING':
            self.draw_playing_ui()

        if self.game.mode == 'LEVEL_UP':
            self.draw_level_up_ui()
        
        if self.game.mode not in ('PLAYING', 'LEVEL_UP'):
            self.draw_static_ui()

    def draw_playing_ui(self):
        """Draw playing ui"""
        self.update_score_visibility()

        elements = (('high_score', *UI_LAYOUT['high_score']), 
                    ('lives', *UI_LAYOUT['lives']), ('current_level', *UI_LAYOUT['current_level']))
        
        for value, pos, align, padded in elements:
            self.draw_text(value, pos, align, padded)

    def draw_level_up_ui(self):
        """Draw level_up ui"""
        if self.level_status == 'show':
            
            elements = (('score', *UI_LAYOUT['score']), ('high_score', *UI_LAYOUT['high_score']), 
                    ('lives', *UI_LAYOUT['lives']), ('current_level', *UI_LAYOUT['current_level']))
        
            for value, pos, align, padded in elements:
                self.draw_text(value, pos, align, padded)

            if self.blink('level', TIMERS['level_up_blink_on']):
                self.level_status = 'hide'
                self.current_time = pygame.time.get_ticks()
        else:
            if self.blink('level', TIMERS['level_up_blink_off']):
                self.level_status = 'show'
                self.current_time = pygame.time.get_ticks()

    def draw_static_ui(self):
        """Draw static ui"""
        elements = (('score', *UI_LAYOUT['score']), ('high_score', *UI_LAYOUT['high_score']), 
                    ('lives', *UI_LAYOUT['lives']), ('current_level', *UI_LAYOUT['current_level']))
        
        for value, pos, align, padded in elements:
            self.draw_text(value, pos, align, padded)

    def draw_text(self, value, pos, align='left', padded=True):
        value = getattr(self.game, value)
        
        if padded:
            text = f'{value:03d}'
        else:
            text = str(value)

        text_surface = self.font.render(text, True, 'white')

        if align == 'right':
            text_rect = text_surface.get_rect(topright=(pos))
        else:
            text_rect = text_surface.get_rect(topleft=(pos))

        self.surface.blit(text_surface, text_rect)

    def blink(self, key, interval):
        if pygame.time.get_ticks() - self.timers[key] >= interval:
            self.timers[key] = pygame.time.get_ticks()
            return True
        return False

    def update_score_visibility(self):
        """Update score visibility"""
        if self.score_status == 'show':
            pos, align, padded = UI_LAYOUT['score']
            self.draw_text('score', pos, align, padded)

            if self.blink('score', TIMERS['score_blink_on']):
                self.score_status = 'hide'
                self.current_time = pygame.time.get_ticks()
        else:
            if self.blink('score', TIMERS['score_blink_off']):
                self.score_status = 'show'
                self.current_time = pygame.time.get_ticks()