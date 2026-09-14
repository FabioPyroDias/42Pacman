"""High score management module for the Pacman project.

Handles loading, validating, updating, and persisting player high scores
to a JSON file, maintaining a validated top 10 leaderboard.
"""

import json


class Highscore():
    """Manages loading, validating, updating, and saving player highscores.

    Maintains a top 10 leaderboard sorted in descending order by score,
    performing rigorous validation on all loaded file entries in a JSON file.

    Attributes:
        path (str): The file path to the JSON high scores storage file.
        scores (list[dict[str, str | int]]): The list containing the validated
            top high scores, sorted in descending order.
    """

    def __init__(self, path: str) -> None:
        """Initializes the manager and loads scores from the specified path.

        Attempts to read and validate the JSON high score list.
        If the file is missing, malformed, or contains invalid data entries,
            handles the errors gracefully and initializes
            an empty high score list.

        Args:
            path (str): The file path to the JSON high scores storage file.

        Returns:
            None
        """

        self.path = path
        self.scores: list[dict[str, str | int]] = []

        try:
            with open(self.path, "r") as save:
                highscores = json.load(save)
            if isinstance(highscores, list):
                for entry in highscores:
                    if not isinstance(entry, dict):
                        print(f"Entry {entry} invalid. Ignoring it...")
                        continue

                    if entry.get("name", None) is None:
                        print(f"Entry {entry} invalid, Ignoring it...")
                        continue
                    else:
                        if not isinstance(entry["name"], str):
                            print(f"Entry {entry} invalid, Ignoring it...")
                            continue

                        if not self.validate_name(entry["name"]):
                            print(f"Entry {entry} invalid, Ignoring it...")
                            continue

                    if not entry.get("score", None):
                        print(f"Entry {entry} invalid, Ignoring it...")
                        continue
                    else:
                        if not isinstance(entry["score"], int):
                            print(f"Entry {entry} invalid, Ignoring it...")
                            continue

                        if entry["score"] < 0:
                            print(f"Entry {entry} invalid, Ignoring it...")
                            continue

                    self.scores.append(entry)
            else:
                print("Invalid format in highscores file. Using empty list")

            return

        except IsADirectoryError:
            error_message = f"{path} is a directory, expected file."
        except FileNotFoundError:
            error_message = f"File {path} not found."
        except PermissionError:
            error_message = f"No permission for {path}."
        except (json.JSONDecodeError, TypeError, AttributeError):
            error_message = "JSON file  wrongly formatted."
        except (OSError, ValueError) as error:
            error_message = f"Unexpected error - {error}"
        except IndexError as error:
            error_message = f"{error}"

        print(f"ERROR (highscore): {error_message}\nUsing empty list")

    def qualifies_highscore(self, score: int) -> bool:
        """Determines if a given score qualifies for the top 10 leaderboard.

        Args:
            score (int): The integer score achieved by the player.

        Returns:
            bool: True if the score is non negative and either the leaderboard
                has fewer than 10 entries or beats at least one
                existing score. False otherwise.
        """

        if score < 0:
            return False

        if len(self.scores) < 10:
            return True

        for entry in self.scores:
            if int(entry["score"]) < score:
                return True

        return False

    def validate_name(self, player_name: str) -> bool:
        """Validates if a player name meets the required formatting rules.

        A valid name cannot be empty, needs to contain 10 characters or fewer,
            and consist exclusively of alphanumeric characters or spaces.

        Args:
            player_name (str): The name provided by the player.

        Returns:
            bool: True if the name passes all criteria. False otherwise.
        """

        if not player_name:
            return False

        if len(player_name) > 10:
            return False

        for character in player_name:
            if not (character.isalnum() or character == " "):
                return False

        return True

    def add_score(self, player_name: str, score: int) -> None:
        """Adds a new score entry, sorting and keeping the top 10.

        Args:
            player_name (str): The name of the player who achieved the score.
            score (int): The score achieved.

        Returns:
            None
        """

        self.scores.append({"name": player_name, "score": score})
        self.scores = sorted(self.scores,
                             key=lambda entry: entry["score"],
                             reverse=True)
        self.scores = self.scores[0: 10]

    def save_highscore(self) -> None:
        """Saves the current top 10 high scores list to the JSON storage file.

        Catches and reports any operating system errors
            encountered during writing.

        Args:
            None

        Returns:
            None
        """

        try:
            with open(self.path, "w") as save:
                json.dump(self.scores, save)
        except OSError:
            print("ERROR (highscore): Couldn't save highscores")
