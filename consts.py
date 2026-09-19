"""Default configurations and game constants for Pacman."""

from typing import Any
from enums import Direction

# Default Configs
SAFE_DEFAULTS: dict[str, Any] = {
    "highscore_filename": "highscores.json",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 99999999999999
}

# Bounding Box of 42 Pattern
PATTERN_42_CELL_COUNT = 18
MAZE_CORNERS = 4

# Level Dimensions range
MIN_DIMENSIONS = 9
MAX_DIMENSIONS = 22

# Lives range
MIN_LIVES = 1
MAX_LIVES = 10

# Pacgums points range
MIN_POINTS_PACGUM = 5
MAX_POINTS_PACGUM = 20

# Super Pacgums points range
MIN_POINTS_SUPER_PACGUM = 25
MAX_POINTS_SUPER_PACGUM = 100

# Points per Ghost range
MIN_POINTS_GHOST = 150
MAX_POINTS_GHOST = 250

# Time range
MIN_LEVEL_TIME = 300
MAX_LEVEL_TIME = 600

FPS = 60
FRAME_DURATION = 1/FPS
ANIMATION_FPS = 12
CTA_BLINK_INTERVAL = 0.5
MAX_SCORE_DIGITS = 16

EXPECTECTED_HIGHSCORES_LEN = 100

# COLORS
BACKGROUND_COLOR = (0, 0, 30)
FT_BACKGROUND_COLOR = (40, 40, 100)
WALL_COLOR = (255, 255, 255)
COMMOM_TEXT_COLOR = (255, 255, 255)
GAME_TITLE_COLOR = (230, 230, 50)
GAME_OVER_TEXT_COLOR = (255, 0, 0)
VICTORY_TEXT_COLOR = (230, 230, 50)
TEXT_BOX_BACKGROUND_COLOR = (30, 30, 30)
GO_COLOR = (40, 230, 40)
READY_COLOR = (230, 40, 40)
NUMBERS_COLOR = (230, 230, 40)

# SIZES
MENU_WIN_SIZE = (800, 600)
SPRITE_SIZE = 40
WALL_THICKNESS = 1
LIFE_ICON_SPACING = 30
FOOTER_MARGIN_BOTTOM = 20
WALL_OFFSET = WALL_THICKNESS * 2
CELL_SIZE = SPRITE_SIZE + WALL_THICKNESS * 4

# SPRITES
PACMAN_SPRITE_LAST_INDEX_X = 3
PACMAN_DEATH_SPRITE_START_INDEX_Y = 4
PACMAN_DEATH_SPRITE_LAST_INDEX_Y = 7
GHOST_SPRITE_LAST_INDEX_X = 1
ENTITIES_UP_SPRITE_INDEX_Y = 0
ENTITIES_RIGHT_SPRITE_INDEX_Y = 1
ENTITIES_LEFT_SPRITE_INDEX_Y = 2
ENTITIES_DOWN_SPRITE_INDEX_Y = 3
DEAD_GHOST_SPRITE_LAST_INDEX_X = 0
SCARED_GHOST_SPRITE_INDEX_Y = 0
FLASHING_GHOST_SPRITE_INDEX_Y = 1

# SPRITE PATH
PACMAN_SPRITE_PATH = "assets/pacman.xpm"
BLINKY_SPRITE_PATH = "assets/blinky.xpm"
CLYDE_SPRITE_PATH = "assets/clyde.xpm"
INKY_SPRITE_PATH = "assets/inky.xpm"
PINKY_SPRITE_PATH = "assets/pinky.xpm"
PACGUM_SPRITE_PATH = "assets/pacgum.xpm"
SUPER_PACGUM_SPRITE_PATH = "assets/super_pacgum.xpm"
LIFE_ICON_SPRITE_PATH = "assets/pacman_life.xpm"
DEAD_GHOST_SPRITE_PATH = "assets/dead_ghost.xpm"
SCARED_GHOST_SPRITE_PATH = "assets/scared_ghost.xpm"

# INSTRUCTIONS
EXPECTECTED_CONTROLS_LEN = 50
CONTROLS_LIST = [
    ("W / Arrow Up ", " Move Up"),
    ("A / Arrow Left ", " Move Left"),
    ("S / Arrow Down ", " Move Down"),
    ("D / Arrow Right ", " Move Right"),
    ("SPACE ", " Play / Pause"),
    ("V ", " Toggle Invincible"),
    ("F ", " Freeze ghosts and timer"),
    ("L ", " Add Lives"),
    ("N ", " Skip Level"),
    ("H ", " View Highscores"),
    ("ESC (Main Menu) ", " Exit Game"),
    ("ESC (Paused) ", " Return to Main Menu"),
]
INSTRUCTIONS_LIST = [
    ("Objective ", "Eat all pacgums to win the level"),
    ("Game Win ", "Complete all levels to win the game"),
    ("Pacgum ", "+X points when eaten"),
    ("Super-pacgum ", "+Y points, makes ghosts edible for a short time"),
    ("Edible Ghost ", "+Z points when eaten"),
    ("Lives ", "Start with +L, lose one when touched by a non-edible ghost"),
    ("Respawn ", "Return to the middle of the maze after losing a life"),
    ("Game Over ", "When all lives are lost"),
    ("Level Timer ", "Each level has a time limit"),
    ("Pause ", "Player can pause and resume during the game")
]

PACMAN_DEATH_ANIMATION_DURATION = 1.28
DEATH_FREEZE_DURATION = 0.45

TIMER_RESPAWN = PACMAN_DEATH_ANIMATION_DURATION + DEATH_FREEZE_DURATION

# There's 4 waves of Scatter and Chase in a game.
# Each of these indexes represent each wave.
# Each index has the duration for each state.
WAVE_TIMERS_SCATTER_CHASE = [
    (7.0, 20.0),
    (7.0, 20.0),
    (5.0, 20.0),
    (5.0, float("inf"))
]

# Global duration after pacman eats a Super Pacgum
TIMER_FRIGHTENED = 10.0

# Time it takes for eaten Ghost to respawn
TIMER_EATEN = 5.0

# Representing movement for each cardinal direction.
DIRECTION_VECTORS: dict[Direction, tuple[float, float]] = {
    Direction.NORTH: (0.0, -1.0),
    Direction.SOUTH: (0.0, 1.0),
    Direction.EAST: (1.0, 0.0),
    Direction.WEST: (-1.0, 0.0),
}

# Maximum Euclidean distance between entities to trigger a collision
COLLISION_DISTANCE_THRESHOLD = 0.5
ENTITY_SPEED = 2

READY_STEP_DURATION = 0.4
READY_TOTAL_DURATION = READY_STEP_DURATION * 7
RESULT_SCREEN_TEXT_DURATION = 1.0

MIN_MAZE_SIZE_FOR_42 = 14
