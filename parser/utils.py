"""Utility functions for validating configuration fields."""

from typing import Any
from consts import SAFE_DEFAULTS, PATTERN_42_CELL_COUNT, MAZE_CORNERS


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
    dictionary containing valid 'width' (14-32), 'height' (14-32), and
    'number_of_pacgums' (width * height - PATTERN_42_CELL_COUNT - MAZE_CORNERS)
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

        value_min_dimensions = SAFE_DEFAULTS["level"][0]["width"]
        value_max_dimensions = (
            SAFE_DEFAULTS["level"][len(SAFE_DEFAULTS["level"]) - 1]["width"])

        if not isinstance(value_width, int):
            return False
        if (value_width < value_min_dimensions
           or value_width > value_max_dimensions):
            return False

        if not isinstance(value_height, int):
            return False
        if (value_height < value_min_dimensions
           or value_height > value_max_dimensions):
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
    Validates player lives count (1 to 10).

    Args:
        value (Any): The player lives to validate.

    Returns:
        bool: True if configuration is between 1 and 10,
                False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < 1 or value > 10:
        return False
    return True


def is_valid_points_per_pacgum(value: Any) -> bool:
    """
    Validates points awarded per pacgum (5 to 20).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between 5 and 20, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < 5 or value > 20:
        return False
    return True


def is_valid_points_per_super_pacgum(value: Any) -> bool:
    """
    Validates points awarded per super pacgum (25 to 150).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between 25 and 150, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < 25 or value > 150:
        return False
    return True


def is_valid_points_per_ghost(value: Any) -> bool:
    """
    Validates points awarded per ghost (150 to 500).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between 150 and 500, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < 150 or value > 500:
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
    Validates maximum level time limit in seconds (60 to 180).

    Args:
        value (Any): The value to validate.

    Returns:
        bool: True if integer between 60 and 180, False otherwise.
    """

    if not isinstance(value, int):
        return False
    if value < 60 or value > 180:
        return False
    return True
