import json


class Highscore():
    def __init__(self, path: str) -> None:
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
        if score < 0:
            return False

        if len(self.scores) < 10:
            return True

        for entry in self.scores:
            if int(entry["score"]) < score:
                return True

        return False

    def validate_name(self, player_name: str) -> bool:
        if not player_name:
            return False

        if len(player_name) > 10:
            return False

        for character in player_name:
            if not (character.isalnum() or character == " "):
                return False

        return True

    def add_score(self, player_name: str, score: int) -> None:
        self.scores.append({"name": player_name, "score": score})
        self.scores = sorted(self.scores,
                             key=lambda entry: entry["score"],
                             reverse=True)
        self.scores = self.scores[0: 10]

    def save_highscore(self) -> None:
        try:
            with open(self.path, "w") as save:
                json.dump(self.scores, save)
        except OSError:
            print("ERROR (highscore): Couldn't save highscores")
