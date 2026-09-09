"""Game enumeration definitions."""
from enum import Enum


class Direction(Enum):
    """Represents cardinal movement directions."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class GhostState(Enum):
    """Represents the states of a Ghost's AI controller."""

    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    EATEN = 3


class GameState(Enum):
    """Represents the global states of the game."""

    PLAYING = 0
    PAUSED = 1
    RESPAWNING = 2
    RESTART_LEVEL = 3
    LEVEL_COMPLETE = 4
    GAME_OVER = 5
    VICTORY = 6
