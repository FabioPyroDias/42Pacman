"""Removes comments and parses config files.

Loads and parses the configuration file.
It ensures safe execution by handling missing, unreadable or malformed
files by using default settings.
"""

from typing import Any
from parser.utils import (is_valid_highscore_filename,
                          is_valid_level, is_valid_lives,
                          is_valid_points_per_pacgum,
                          is_valid_points_per_super_pacgum,
                          is_valid_points_per_ghost,
                          is_valid_seed,
                          is_valid_level_max_time)
from consts import (SAFE_DEFAULTS, PATTERN_42_CELL_COUNT, MAZE_CORNERS,
                    MIN_DIMENSIONS, MAX_DIMENSIONS)
import re
import json


def parser_configuration_file(path: str) -> dict[str, Any]:
    """
    Parses a JSON configuration file and returns validated settings.

    Reads the file at the given path, removes comments, and parses the JSON
    content.
    If the file is missing, unreadable, or malformed, it catches the error,
    prints a warning and returns safe default configurations.

    Args:
        path (str): The file system path to the configuration file.

    Returns:
        dict[str, Any]: The parsed validted configuration.
    """

    # This will hold the specific error found to be printed
    error_message = ""
    # Correct expected fields and values for the game
    configs: dict[str, Any] = {}

    try:
        with open(path, "r") as fd:
            # The workflow is quite simple:
            # 1 - Read everythng from the config file.
            # 2 - Remove possible comments, both inline and block.
            # 3 - Parse text to dictionary format
            # 4 - Validate fields and values.
            # If in any step there's an error, the error message is printed
            #   and the configs will go to 'correct_configs', which will
            #   validate what is right and correct what is wrong.
            # This is needed since the subject demands faulty configs
            #   will not crash the game and will be clamped to "safe defaults"
            content = fd.read()
            filtered_content = remove_comments(content)
            configs = json.loads(filtered_content)
            validate_configs(configs)
            return configs
    except IsADirectoryError:
        error_message = f"{path} is a directory, expected file."
    except FileNotFoundError:
        error_message = f"File {path} not found."
    except PermissionError:
        error_message = f"No permission for {path}."
    except (json.JSONDecodeError, TypeError):
        error_message = "JSON file  wrongly formatted."
    except (OSError, ValueError) as error:
        error_message = f"Unexpected error - {error}"
    except IndexError as error:
        error_message = f"{error}"

    print(f"ERROR: {error_message}\nUsing default values...")

    return correct_configs(configs)


def remove_comments(content: str) -> str:
    """
    Removes block and inline comments from a given string.

    Args:
        content (str): The configuration string.

    Returns:
        str: The filtered configuration string with all comments removed.
    """

    filtered_content = ""

    # To remove the possible block comments from the configuration file,
    #   the process is divided into three parts:
    # 1 - '/\*' - Locates the exact beginnig of the comment "/*".
    #   The backslash '\' before the asterix '*' acts as an escape character.
    #   This is required since the asterix is a special character in regex.
    # 2 - '.*?' - Matches any character along the along the way.
    #   . represents any character
    #   *? enables non-greedy behaviour.
    #   This guarantees the search stops as soon as the first '*/'
    #       is found.
    #   The greedy behaviour would look for the last instance of '*/',
    #       assuming everything was between the block comment.
    # 3 - '*/' - The end of the block comment.
    #
    # The re.DOTALL specifies the lookup for the pattern doesn't stop when
    #   it finds a newline character. By default, that would be the behaviour.
    content_without_block_comment = re.sub(r'/\*.*?\*/', '',
                                           content, flags=re.DOTALL)

    # Since we're only looking for inline comments, lines with
    #   '#' or '//', we split the content by line.
    content_split = content_without_block_comment.split("\n")

    # Iterating through the lines.
    # The rest of the line will be discarded.
    for line in content_split:
        # If there are no comment characters, the entire line is added
        #   to the filtered_context
        if line.find("//") == -1 and line.find("#") == -1:
            filtered_content += line

        # If there is at least one comment character, both
        #   cases are found, '#' and '//', and the line is filtered
        #   from the beginning to that index.
        # By doing this, we can have inline comments at the end of the
        #   line without it removing entirely.
        else:
            hash_index = line.find("#")
            slash_index = line.find("//")
            selected_character_index = 0
            if hash_index == -1:
                selected_character_index = slash_index
            elif slash_index == -1:
                selected_character_index = hash_index
            else:
                selected_character_index = min(hash_index, slash_index)
            filtered_content += line[0:selected_character_index]

    return filtered_content


def validate_configs(configs: dict[str, Any]) -> None:
    """
    Validates the configuration dictionary structure and values.

    Checks if all required fields are present, if no unexpected extra fields
    exist, and if the configuration values are valid.

    Args:
        configs (dict[str, Any]): The configuration dictionary to validate.

    Returns:
        None

    Raises:
        IndexError
    """

    # Testing "highscore_filename"
    if not is_valid_highscore_filename(configs.get("highscore_filename", "")):
        raise IndexError("Invalid JSON field \'highscore_filename\'")

    # Testing "level"
    if not is_valid_level(configs.get("level", "")):
        raise IndexError("Invalid JSON field \'level\'")

    # Testing "lives"
    if not is_valid_lives(configs.get("lives", "")):
        raise IndexError("Invalid JSON field \'lives\'")

    # Testing "points_per_pacgum"
    if not is_valid_points_per_pacgum(configs.get("points_per_pacgum", "")):
        raise IndexError("Invalid JSON field \'points_per_pacgum\'")

    # Testing "points_per_super_pacgum"
    if not is_valid_points_per_super_pacgum(
      configs.get("points_per_super_pacgum", "")):
        raise IndexError("Invalid JSON field \'points_per_super_pacgum\'")

    # Testing "points_per_ghost"
    if not is_valid_points_per_ghost(configs.get("points_per_ghost", "")):
        raise IndexError("Invalid JSON field \'points_per_ghost\'")

    # Testing "seed"
    if not is_valid_seed(configs.get("seed", "")):
        raise IndexError("Invalid JSON field \'seed\'")

    # Testing "level_max_time"
    if not is_valid_level_max_time(configs.get("level_max_time", "")):
        raise IndexError("Invalid JSON field \'level_max_time\'")


def correct_configs(wrong_configs: dict[str, Any]) -> dict[str, Any]:
    """
    Corrects configuration values using safe defaults.

    Iterates through expected configuration keys, retaining valid user values
    and replacing missing, malformed, or invalid parameters with their
    corresponding entry from SAFE_DEFAULTS.
    Extra unexpected keys are ignored.

    Args:
        wrong_configs (dict[str, Any]): The raw configuration dictionary.

    Returns:
        dict[str, Any]: A corrected configuration dictionary containing
            only valid keys and values.
    """

    if not wrong_configs:
        return SAFE_DEFAULTS

    corrected_configs = {}

    # Correcting "highscore_filename"
    if is_valid_highscore_filename(
      wrong_configs.get("highscore_filename", "")):
        corrected_configs["highscore_filename"] = (
            wrong_configs["highscore_filename"])
    else:
        corrected_configs["highscore_filename"] = (
            SAFE_DEFAULTS["highscore_filename"])

    # Correcting "level"
    if not is_valid_level(wrong_configs.get("level", "")):
        level = wrong_configs.get("level", "")

        if isinstance(level, list):

            levels = []
            index = 0
            while index < len(level):
                current_level = {}

                value_width = level[index].get("width", "")
                value_height = level[index].get("height", "")
                value_number_of_pacgums = (
                    level[index].get("number_of_pacgums", ""))

                if (not isinstance(value_width, int)
                   or value_width < MIN_DIMENSIONS
                   or value_width > MAX_DIMENSIONS):
                    current_level["width"] = (
                        SAFE_DEFAULTS["level"][index]["width"])
                else:
                    current_level["width"] = value_width

                if (not isinstance(value_height, int)
                   or value_height < MIN_DIMENSIONS
                   or value_height > MAX_DIMENSIONS):
                    current_level["height"] = (
                        SAFE_DEFAULTS["level"][index]["height"])
                else:
                    current_level["height"] = value_height

                # The maximum number of pacgums must include both the
                #   "42 pattern" in the center of the maze and the 4
                #   corners where the super pacgums will exist.
                # These are constants in the 'consts.py'.
                # But levels might not be perfect squares. Per example
                #   width = 16 and height = 28.
                # In this case, 'number_of_pacgums' needs to be
                #   16 * 28 - PATTERN_42_CELL_COUNT - MAZE_CORNERS.
                # This way, all valid cells have a pacgum instead of
                #   the 42 pattern and corners where super pacgums exist.
                max_pacgums = (
                    current_level["width"] * current_level["height"]
                    - PATTERN_42_CELL_COUNT - MAZE_CORNERS)

                if (not isinstance(value_number_of_pacgums, int)
                   or value_number_of_pacgums != max_pacgums):
                    current_level["number_of_pacgums"] = max_pacgums
                else:
                    current_level["number_of_pacgums"] = (
                        value_number_of_pacgums)

                levels.append(current_level)
                index += 1

            # In case there are levels missing
            while index < len(SAFE_DEFAULTS["level"]):
                levels.append(SAFE_DEFAULTS["level"][index])
                index += 1

            corrected_configs["level"] = levels

        else:
            corrected_configs["level"] = SAFE_DEFAULTS["level"]
    else:
        corrected_configs["level"] = wrong_configs["level"]

    # Correcting "lives"
    if is_valid_lives(wrong_configs.get("lives", "")):
        corrected_configs["lives"] = wrong_configs["lives"]
    else:
        corrected_configs["lives"] = SAFE_DEFAULTS["lives"]

    # Correcting "points_per_pacgum"
    if is_valid_points_per_pacgum(wrong_configs.get("points_per_pacgum", "")):
        corrected_configs["points_per_pacgum"] = (
            wrong_configs["points_per_pacgum"])
    else:
        corrected_configs["points_per_pacgum"] = (
            SAFE_DEFAULTS["points_per_pacgum"])

    # Correcting "points_per_super_pacgum"
    if is_valid_points_per_super_pacgum(
      wrong_configs.get("points_per_super_pacgum", "")):
        corrected_configs["points_per_super_pacgum"] = (
            wrong_configs["points_per_super_pacgum"])
    else:
        corrected_configs["points_per_super_pacgum"] = (
            SAFE_DEFAULTS["points_per_super_pacgum"])

    # Correcting "points_per_ghost"
    if is_valid_points_per_ghost(wrong_configs.get("points_per_ghost", "")):
        corrected_configs["points_per_ghost"] = (
            wrong_configs["points_per_ghost"])
    else:
        corrected_configs["points_per_ghost"] = (
            SAFE_DEFAULTS["points_per_ghost"])

    # Correcting "seed"
    if is_valid_seed(wrong_configs.get("seed", "")):
        corrected_configs["seed"] = wrong_configs["seed"]
    else:
        corrected_configs["seed"] = SAFE_DEFAULTS["seed"]

    # Correcting "level_max_time"
    if is_valid_level_max_time(wrong_configs.get("level_max_time", "")):
        corrected_configs["level_max_time"] = wrong_configs["level_max_time"]
    else:
        corrected_configs["level_max_time"] = SAFE_DEFAULTS["level_max_time"]

    return corrected_configs
