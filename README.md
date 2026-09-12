*This project has been created as part of the 42 curriculum by fda-cruz, jsouza.*

## Description

Pacman is recreation of the classic 1980s arcade game. Instead of a default maze, the project integrates an externally provided maze generation package. Another 42 project, A-Maze-ing, built by another group.

The game parameters are defined by a JSON configuration file support single-line comments as well as block comments.
If the configuration file isn't correctly formatted or the configuration itself is invalid, the game corrects what's wrong and fills in what's missing.
There are 10 playable levels. By default, these increase in size as the player progresses through the levels.

The project also implements the four original ghosts:
- Blinky, who chases pacman directly
- Pinky, who ambushes pacman
- Inky, who flanks pacman using both pacman's and Blinky's positions
- Clyde, who chases or rans from pacman depending on the distance

The player collects Pacgums and SuperPacums to increase their score. These last ones however, change the ghosts to a Frightened state which pacman can then eat, and score more points. This is the standard behaviour in the original Pacman.

After the game is finished, both by winning or losing, if the score is within the top 10 scores found in the highscore file, the score is stored in the file.

Several cheats were implemented, allowing invincibility, freezing the ghosts in place, skipping levels and adding extra lives.

## Requirements

Make sure `make` is installed on your system:

```bash
sudo apt install make
```

Python 3.10 or higher is required. Check your version with:

```bash
python3 --version
```

Lastly, `uv` is also required:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

A virtual environment (pacman) will be created automatically during installation. This ensures project dependencies are isolated.

## Instructions

### Installation

To install project dependencies, simply run `make install` in the terminal.
This will:
- Create a virtual environment pacman
- Install required Python packages (flake8, mypy, mazegeneratpr, etc.)

### Execution

Run the program with `make run`.

Alternatively, the program can be ran with `pacman/bin/python pacman.py config.json`

## Technical Overview

### Configuration JSON File

The configuration file is JSON, with support for inline comments `#` and `//` as well as block comments `*/ /*`.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `highscore_filename` | **str** | highscores.json | Path to the highscore JSON file |
| `level` | **list[dict[str, int]]** | 10 predefined levels | The entries are `width`, `height` and `number_of_pacgums`. The first two values are clamped between `[14, 32]` |
| `lives` | **int** | 3 | Clamped to `[1, 10]` |
| `points_per_pacgum` | **int** | 10 | Clamped to `[5, 20]` |
| `points_per_super_pacgum` | **int** | 50 | Clamped to `[25, 100]` |
| `points_per_ghost` | **int** | 200 | Clamped to `[150, 250]` |
| `seed` | **int** | 42 | Used to generate the level 1 maze deterministically |
| `level_max_time` | **int** | 90 (seconds) | Clamped to `[60, 180]` |

The `number_of_pacgums` per level is calculated with: `width * height - 18 - 4`.

`18` due to the size square area of the 42 pattern and `4` represents all the corners reserved for `SuperPacgums`.
This formula is automatically executed in case the config value doesn't match.

Any missing, malformed or out of range value is replaced with it's safe default, entry by entry. This means that a single wrong field does not discard the whole file. Unknown keys are ignored. Any parsing or validation error never crashes the program.

### Highscore system

Highscores are stored locally in a JSON file, keeping only the top 10 results.

All entries are validated upon loading. Any malformed or invalid record is filtered out and removed when the file is next saved.

When the game ends, wether by losing all lives or completing all levels, the player can input their name if their score qualifies for the top 10 or if fewer than 10 entries exist. The name cannot be empty, must contain only alphanumeric characters or spaces, and has a maximum length of 10 characters.

Data is stored as a list of dicts `{"name": str, "score": int}`. This format allows multiple entries under the same name without overwriting previous scores.

### Maze Generation

Maze generation is handled by the assigned external **A-Maze-ing** package, ensuring this project does not implement it's own generator.

An adapter class wrapps the package's output to fit the project's needs without modifying the original source code.
This class handles boundary validation and filters unreachable cells, such as the 42 pattern, during pathfinding.

The first level is always generated using the seed set in the config JSON file, while the subsequent levels use random seeds.

### Implementation

Every object in the maze inherits from a base `Entity` class. This only possesses `position`.

`Pacgums` and `SuperPacgums`, share an abstract class `Collectable` with the method `on_collected` that returns scores. `Pacgum` simply returns a dict `{"points": self.points}`, while `SuperPacgum` returns `{"points": self.points, "effect": "frighten"}`.

`Pacman` and the four `Ghosts` subclasses, `Blinky`, `Pinky`, `Inky` and `Clyde`, extend `MovableEntity`, with each ghost overriding `calculate_chase_target` for its respective behaviour.

The collision detection is always `Pacman-Collectable` and `Pacman-Ghost`. Entirely logic based, not pixel base. Two entities collide if they occupy the same cell at the end of a frame or if they cross paths while swapping adjacent cells.

The `Ghosts` cycle through a `SCATTER` and a `CHASE` states waves on a global timer. They switch to `FRIGHTENED` when a `SuperPacgum` is collected, freezing the previously timer. When `Pacman` collides with any of these while in `FRIGHTENED` state, their state's changed to `EATEN`, respawning them after a fixed delay.

A cheat mode was implemented. These are:
- **Invincibility**: The player can collide with `Ghosts` without being in their `FRIGHTENED` state and won't lose any lives or stop the game.
- **Ghost Freeze**: The `Ghosts` stop moving.
- **Level Skip**: The player can simply skip the level and go to the next or, if it's the last level, finish the game.
- **Add Lives**: Everytime the player uses this cheat, they get one more live.

This mode was implement to help the peers review the features of the game easily.

### General Software Architecture

The game logic and rendering are completely independent.

The core game orchestrator, `Game` manages state variables such as `score` and `lives` while instantiating `Pacman`, the four `ghosts`, and `collectables`.
This class possesses the `update` method, which drives the entire game forward on every frame, being responsible for movement, state changes and collisions.

Both `Pacman` and `Ghost` inherit from `MovableEntity` but their decisions to move are very different. While the first is controlled by player input, the latter decide their route autonomously. Due to this, `Game` calls each type of update explicitly rather than treating them polymorphically.

Configuration parsers and highscore modules operate without game dependencies. When transitioning between `levels`, `entities` and `collectables` are freshly re-instantiated rather than reset.

## Project Management

Project management documents are available in the [`project_management/project_management.md`](./project_management/project_management.md) directory.

## Resources

### Original Pacman

- [Original Pac-Man ghost AI reference (Pac-Man Dossier)](https://www.gamedeveloper.com/design/the-pac-man-dossier)

### Use of AI

Claude was used early on to help structure the project and clarify conceptual questions.

Gemini was used to assist with project documentation and concept research.

The overall flow and structure of the project were already planned by the student, but AI was used to double-check that nothing important was being left out during the implementation.