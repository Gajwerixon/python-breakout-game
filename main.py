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

        self.mode = 'ATTRACT'
        self.mode_start = None

        self.lives = 3
        self.current_level = 1
        self.high_score = 0
        self.score = 0
        self.hits = 0
        
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.level = Level(self.surface, self.all_sprites, self.obstacles)
        self.paddle = Paddle(self, self.all_sprites, self.obstacles, full_width=True)
        self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)

        self.ui = UI(self)
        self.sounds = self.load_sounds()

        self.level.generate_attract_layout()

    def run_game(self):
        """Main game loop"""
        while True:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.mode == 'ATTRACT':
                    self.start_game()
                    self.mode = 'RESET_ROUND'

    def update(self, dt):
        """Update game"""
        self.handle_timers()

        if self.mode == 'PLAYING':
            self.handle_ball_loss()
            self.update_difficulty()
            self.next_level()

        self.all_sprites.update(dt)

    def draw(self):
        """Draw on screen"""
        self.surface.fill('black')

        self.all_sprites.draw(self.surface)

        self.ui.draw()

        pygame.display.flip()

    def handle_timers(self):
        """Handle timers"""
        if self.mode == 'RESET_ROUND':
            if pygame.time.get_ticks() - self.mode_start >= TIMERS['ball_spawn']:
                self.ball.reset()
                self.mode = 'PLAYING'
        
        if self.mode == 'RESET_GAME':
            if pygame.time.get_ticks() - self.mode_start >= TIMERS['reset_game']:
                self.ball.reset()
                self.mode = 'ATTRACT'

        if self.mode == 'LEVEL_UP':
            if pygame.time.get_ticks() - self.mode_start > TIMERS['level_up']:
                self.level.generate_normal_layout()
                self.mode = 'PLAYING'

    def handle_ball_loss(self):
        """Handle if ball goes under screen"""        
        if self.ball.rect.top <= HEIGHT:
            return
        
        if self.mode == 'PLAYING' and self.ball.rect.top >= HEIGHT:
            self.lives -= 1
            self.ball.hide()
        
        if self.lives > 0 and self.mode != 'RESET_ROUND':
            self.mode = 'RESET_ROUND'
            self.reset_round()
        
        if self.lives == 0 and self.mode != 'RESET_GAME':
            self.mode = 'RESET_GAME'
            self.enter_game_over_state()

    def update_difficulty(self):
        """Update difficulty base on two conditions"""
        self.handle_speed_progression()
        if self.ball.is_above_bricks and not self.paddle.shrinked:
            self.paddle.build_paddle(self.paddle.get_current_pos(), True)
            self.paddle.shrinked = True

    def handle_speed_progression(self):
        """Handle speed progression base on hits and current score"""
        if self.hits in (4, 10, 20):
            self.ball.increase_speed(self.score)
            self.ball.speed_stage_ready = False
        else:        
            self.ball.speed_stage_ready = True

    def next_level(self):
        """If the play destroy all bricks, create next level"""
        if self.level.bricks_remaining != 0:
            return
        
        if self.mode == 'PLAYING':
            self.play_sounds('win')
            self.ui.level_up = True

            self.paddle.build_paddle(self.paddle.get_current_pos())

            self.current_level += 1
            self.hits = 0

            self.mode = 'LEVEL_UP'
            self.mode_start = pygame.time.get_ticks()

    def start_game(self):
        """Start game """
        self.level.reset_bricks()

        self.save_high_score()

        self.current_level = 1
        self.lives = 3
        self.score = 0    
        self.hits = 0
        
        self.paddle.build_paddle()

        self.ball.hide()

        self.mode_start = pygame.time.get_ticks()

    def reset_round(self):
        """Reset round"""
        if self.paddle.shrinked:
            self.paddle.build_paddle(self.paddle.get_current_pos())
            self.paddle.shrinked = False
        
        self.hits = 0

        self.mode_start = pygame.time.get_ticks()

    def enter_game_over_state(self):
        """Intermidate stage between player loss and new game"""
        self.paddle.build_paddle(full_width=True)
        
        # --- Waiting for 2.5 second and create new ball ---
        self.mode_start = pygame.time.get_ticks()

    def save_high_score(self):
        """Save high score"""
        if self.score > self.high_score:
            self.high_score = self.score

    def load_sounds(self):
        """Load sounds"""
        sounds = {
        'wall':   pygame.mixer.Sound('assets/sound_effects/wall_hit_sound.mp3'),
        'brick':  pygame.mixer.Sound('assets/sound_effects/brick_hit_sound.mp3'),
        'paddle': pygame.mixer.Sound('assets/sound_effects/paddle_hit_sound.mp3'),
        'win':    pygame.mixer.Sound('assets/sound_effects/win_sound.mp3'),
        }

        for sound in sounds.values():
            sound.set_volume(0.2)
        
        return sounds

    def play_sounds(self, name):
        """Play sound of the given name"""
        if name in self.sounds:
            self.sounds[name].play()

game = Game()
game.run_game()