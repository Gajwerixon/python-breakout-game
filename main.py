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
        self.lives = 3
        self.current_level = 1
        self.high_score = 0
        self.score = 0
        self.hits = 0

        # --- Timers ---
        self.round_reset_timer = None
        self.spawn_ball = None
        self.restart_delay_timer = None
        self.level_up = None
        
        # --- Sprites ---
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.level = Level(self.surface, self.all_sprites, self.obstacles)
        self.paddle = Paddle(self.all_sprites, self.obstacles)
        self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)

        # --- Initialize game ---
        self.level.initialize_game()
        self.ui = UI(self.surface)

        self.sounds = self.load_sounds()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_active:
                    self.reset_game()

    def update(self, dt):
        """Update game"""
        self.handle_ball_loss()

        self.handle_timers()
        
        if self.ball and self.game_active:
            self.update_difficulty()

        self.next_level()

        self.all_sprites.update(dt)

    def handle_ball_loss(self):
        """Handle if ball goes under screen"""
        if not self.ball:
            return

        if self.ball.rect.top <= HEIGHT:
            return

        self.lives -= 1

        self.ball.kill()
        self.ball = None

        current_time = pygame.time.get_ticks()
        if self.lives > 0:
            self.round_reset_timer = current_time
        else:
            self.game_active = False
            self.prepare_restart()

    def next_level(self):
        if self.score / self.current_level != 448:
            return
        
        if not self.level_up:
            self.play_sounds('win')
            self.ui.level_up = True

            self.ball.kill()

            paddle_pos = self.paddle.get_current_pos()
            self.paddle.kill()

            self.paddle = Paddle(self.all_sprites, self.obstacles, paddle_pos)

            self.current_level += 1
            self.hits = 0

            self.level_up = pygame.time.get_ticks()

    def prepare_restart(self):
        """This is intermidate stage between player loss and restart of the new game"""
        self.paddle.kill()
        self.paddle = Paddle(self.all_sprites, self.obstacles, full_width=True)
        self.paddle.active = False
        
        # --- Handle timers is waiting for 1.5 secound and create new ball ---
        self.restart_delay_timer = pygame.time.get_ticks()

    def update_difficulty(self):
        """Update difficulty base on two conditions"""
        self.handle_speed_progression()
        if self.ball.is_above_bricks():
            self.paddle.shrink()

    def handle_speed_progression(self):
        """Handle speed progression base on hits and current score"""
        if self.hits in (4, 10, 20):
            self.ball.increase_speed(self.score)
            self.ball.speed_stage_ready = False
        else:        
            self.ball.speed_stage_ready = True

    def handle_timers(self):
        """Handle timers"""
        # --- Reset round ---
        if self.round_reset_timer:
            if pygame.time.get_ticks() - self.round_reset_timer > RESET_TIME_ROUNDS:
                self.reset_round()
                self.round_reset_timer = None

        # --- Ball spawn after reset ---
        if self.restart_delay_timer:
            if pygame.time.get_ticks() - self.restart_delay_timer > RESET_TIME_ROUNDS and not self.game_active:
                self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)
                self.ball.launched = False
                self.restart_delay_timer = False
        
        # --- Reset game ---
        if self.spawn_ball:
            if pygame.time.get_ticks() - self.spawn_ball > RESET_TIME_ROUNDS:
                self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)
                self.spawn_ball = None

        if self.level_up:
            if pygame.time.get_ticks() - self.level_up > LEVEL_UP_TIME:
                self.level_up = None
                self.level.reset()
                self.ui.level_up = False
                self.spawn_ball = pygame.time.get_ticks()

    def reset_round(self):
        """Reset round"""
        self.ball = Ball(self, self.paddle, self.all_sprites, self.obstacles)
        self.ball.speed = BALL_START_SPEED
        self.ball.speed_stage_ready = True

        if self.paddle.shrinked:
            old_pos = self.paddle.get_current_pos()
            self.paddle.kill()
            self.paddle = Paddle(self.all_sprites, self.obstacles, old_pos)
            self.paddle.shrinked = False

        self.hits = 0
        self.round_reset_timer = None

    def reset_game(self):
        """Reset game after player loss all 3 lives"""
        if self.ball:
            self.ball.kill()

        self.paddle.kill()

        self.level.reset()

        self.paddle = Paddle(self.all_sprites, self.obstacles)

        self.save_high_score()

        self.current_level = 1
        self.lives = 3
        self.score = 0
        
        self.hits = 0

        self.game_active = True

        self.spawn_ball = pygame.time.get_ticks()

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