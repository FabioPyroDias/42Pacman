"""Default configurations and game constants for Pac-Man."""

from typing import Any


SAFE_DEFAULTS: dict[str, Any] = {
    "highscore_filename": "path_to_file",
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
    "level_max_time": 90
}

PATTERN_42_CELL_COUNT = 18
MAZE_CORNERS = 4

MIN_DIMENSIONS = 14
MAX_DIMENSIONS = 32

MIN_LIVES = 1
MAX_LIVES = 10

MIN_POINTS_PACGUM = 5
MAX_POINTS_PACGUM = 20

MIN_POINTS_SUPER_PACGUM = 25
MAX_POINTS_SUPER_PACGUM = 100

MIN_POINTS_GHOST = 150
MAX_POINTS_GHOST = 250

MIN_LEVEL_TIME = 60
MAX_LEVEL_TIME = 180

# COLORS
BACKGROUND_COLOR = (0, 0, 30)
FT_BACKGROUND_COLOR = (40, 40, 100)
WALL_COLOR = (255, 255, 255)
COMMOM_TEXT_COLOR = (255, 255, 255)
GAME_TITLE_COLOR = (230, 230, 50)

# SIZES
WALL_THICKNESS = 1
WALL_OFFSET = WALL_THICKNESS * 2
CELL_SIZE = 40 + WALL_OFFSET * 2
SPRITE_SIZE = 40

# SPRITES
PLAYER_SPRITE_LAST_INDEX_X = 3
PALYER_DEATH_SPRITE_START_INDEX_Y = 4
PALYER_DEATH_SPRITE_LAST_INDEX_Y = 7
GHOST_SPRITE_LAST_INDEX_X = 1
ENTITIES_UP_SPRITE_INDEX_Y = 0
ENTITIES_RIGHT_SPRITE_INDEX_Y = 1
ENTITIES_LEFT_SPRITE_INDEX_Y = 2
ENTITIES_DOWN_SPRITE_INDEX_Y = 3
