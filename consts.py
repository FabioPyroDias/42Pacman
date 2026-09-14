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
    "level_max_time": 90
}

# Bounding Box of 42 Pattern
PATTERN_42_CELL_COUNT = 18
MAZE_CORNERS = 4

# Level Dimensions range
MIN_DIMENSIONS = 14
MAX_DIMENSIONS = 32

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
MIN_LEVEL_TIME = 60
MAX_LEVEL_TIME = 180

# Seconds it takes for the player to respawn
TIMER_RESPAWN = 2.0

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
