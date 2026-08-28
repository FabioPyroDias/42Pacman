"""Game enumeration definitions."""
from enum import Enum


class Direction(Enum):
    """Represents cardinal movement directions."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
