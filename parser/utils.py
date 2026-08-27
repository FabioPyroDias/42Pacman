"""Utility functions for validating configuration fields."""

from typing import Any
from consts import (SAFE_DEFAULTS, PATTERN_42_CELL_COUNT, MAZE_CORNERS,
                    MIN_DIMENSIONS, MAX_DIMENSIONS,
                    MIN_LIVES, MAX_LIVES, MIN_POINTS_PACGUM,
                    MAX_POINTS_PACGUM, MIN_POINTS_SUPER_PACGUM,
                    MAX_POINTS_SUPER_PACGUM, MIN_POINTS_GHOST,
                    MAX_POINTS_GHOST, MIN_LEVEL_TIME, MAX_LEVEL_TIME)


def is_valid_highscore_filename(value: Any) -> bool:
    """
    Validates the highscore filename.

    Args:
        value (Any): The file name to validate.

    Returns:
        bool: True if it is a non-empty string, False otherwise.
    """

    if not isinstance(value, str):
        return False
    if not value:
        return False
    return True


def is_valid_level(value: Any) -> bool:
    """
    Validates a list of level configurations.

    Checks if the input is a list with at least 10 items, where each item is a
        dictionary containing valid 'width' (MIN_DIMENSIONS - MAX_DIMENSIONS),
        'height' (MIN_DIMENSIONS - MAX_DIMENSIONS), and 'number_of_pacgums'
        (width * height - PATTERN_42_CELL_COUNT - MAZE_CORNERS)
        settings.

    Args:
        value (Any): The level configuration value to validate.

    Returns:
        bool: True if the configuration meets all requirements,
                False otherwise.
    """

    if (not isinstance(value, list)
       or len(value) < len(SAFE_DEFAULTS["level"])):
        return False

    for level in value:
        if not isinstance(level, dict):
            return False

        if len(level.keys()) != len(SAFE_DEFAULTS["level"][0]):
            return False

        value_width = level.get("width", "")
        value_height = level.get("height", "")
        value_number_of_pacgums = level.get("number_of_pacgums", "")

        if not isinstance(value_width, int):
            return False
        if (value_width < MIN_DIMENSIONS
           or value_width > MAX_DIMENSIONS):
            return False

        if not isinstance(value_height, int):
            return False
        if (value_height < MIN_DIMENSIONS
           or value_height > MAX_DIMENSIONS):
            return False

        max_pacgums = (value_width * value_height
                       - PATTERN_42_CELL_COUNT - MAZE_CORNERS)

        if not isinstance(value_number_of_pacgums, int):
            return False
        if value_number_of_pacgums != max_pacgums:
            return False

    return True


def is_valid_lives(value: Any) -> bool:
    """
    Validates player lives count
        (MIN_LIVES to MAX_LIVES).

    Args:
        value (Any): The player lives to validate.

    Returns:
        bool: True if configuration is between MIN_LIVES
            and MAX_LIVES, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < MIN_LIVES or value > MAX_LIVES:
        return False
    return True


def is_valid_points_per_pacgum(value: Any) -> bool:
    """
    Validates points awarded per pacgum
        (MIN_POINTS_PACGUM to MAX_POINTS_PACGUM).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between MIN_POINTS_PACGUM
            and MAX_POINTS_PACGUM, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < MIN_POINTS_PACGUM or value > MAX_POINTS_PACGUM:
        return False
    return True


def is_valid_points_per_super_pacgum(value: Any) -> bool:
    """
    Validates points awarded per super pacgum
        (MIN_POINTS_SUPER_PACGUM to MAX_POINTS_SUPER_PACGUM).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between MIN_POINTS_SUPER_PACGUM
            and MAX_POINTS_SUPER_PACGUM, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < MIN_POINTS_SUPER_PACGUM or value > MAX_POINTS_SUPER_PACGUM:
        return False
    return True


def is_valid_points_per_ghost(value: Any) -> bool:
    """
    Validates points awarded per ghost
        (MIN_POINTS_GHOST to MAX_POINTS_GHOST).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between MIN_POINTS_GHOST
            and MAX_POINTS_GHOST, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < MIN_POINTS_GHOST or value > MAX_POINTS_GHOST:
        return False
    return True


def is_valid_seed(value: Any) -> bool:
    """
    Validates random seed (non-negative integer).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer >= 0, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < 0:
        return False
    return True


def is_valid_level_max_time(value: Any) -> bool:
    """
    Validates maximum level time limit in seconds
        (MIN_LEVEL_TIME to MAX_LEVEL_TIME).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between MIN_LEVEL_TIME
            and MAX_LEVEL_TIME, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < MIN_LEVEL_TIME or value > MAX_LEVEL_TIME:
        return False
    return True
