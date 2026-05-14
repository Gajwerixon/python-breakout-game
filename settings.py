# --- Game ---
WIDTH, HEIGHT = 800, 600

# --- Timers ---
TIMERS = {
    "score_blink_on": 256,
    "score_blink_off": 128,
    "level_up_blink_on": 512,
    "level_up_blink_off": 256,
    "reset_game": 2500,
    "ball_spawn": 2500,
    "level_up": 4000,
}

# --- Paddle ---
PADDLE_WIDTH, PADDLE_HEIGHT = 36, 12
PADDLE_COLOR = (34, 106, 230)
PADDLE_SPEED = 300

# --- Wall ---
WALL_THICKNESS = 12
OFFSET_Y = 64
OFFSET_X = 164
WALL_COLOR = (255, 255, 255)

# --- Bricks ---
BRICK_GRID_COLS = 8
BRICK_GRID_ROWS = 14
ROWS_PER_COLOR = 2

BRICK_COLORS = [(235, 27, 12), (232, 132, 9), (12, 235, 45), (231, 235, 12)]
BRICK_HEIGHT = 12
BRICK_WIDTH = 32

MARGIN_X = OFFSET_X + WALL_THICKNESS
MARGIN_Y = OFFSET_Y + WALL_THICKNESS + 76

# --- Ball ---
BALL_HEIGHT = 6
BALL_WIDTH = 10
BALL_COLOR = ((255, 255, 255))

BALL_START_Y = 360

BALL_START_SPEED = 200
SPEED_MULTIPLEIER = 1.2

# --- User Interface ---
FONT_SIZE =  32

LEVEL_POS_X = OFFSET_X + WALL_THICKNESS
LEVEL_POS_Y = OFFSET_Y + WALL_THICKNESS

SCORE_POS_X = LEVEL_POS_X + 4 * FONT_SIZE
SCORE_POS_Y = LEVEL_POS_Y + FONT_SIZE

LIVES_POS_X = OFFSET_X + WALL_THICKNESS + BRICK_WIDTH * 8
LIVES_POS_Y = LEVEL_POS_Y

HIGH_SCORE_POS_X = LIVES_POS_X + 4 * FONT_SIZE
HIGH_SCORE_POS_Y = LEVEL_POS_Y + FONT_SIZE

UI_LAYOUT = {
    'score': ((SCORE_POS_X, SCORE_POS_Y), 'right', True),
    'high_score': ((HIGH_SCORE_POS_X, HIGH_SCORE_POS_Y), 'right', True),
    'current_level': ((LEVEL_POS_X, LEVEL_POS_Y), 'left', False),
    'lives': ((LIVES_POS_X, LIVES_POS_Y), 'left', False)
}