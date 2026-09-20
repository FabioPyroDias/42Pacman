## Instructions

### Configuration File

The `config.json` file possesses all the fields required to setup the game. If no file is found, the standard configuration will be applied. This also applies to incorrect or malformed fields in the file.

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

### How to Play

Opening the game, there's four keys available to press:
- `ESC` to exit the game
- `H` to check the highscores
- `I` to display the game rules and all the available instructions
- `SPACE` to start the game

The player moves `pacman` with the `WASD` keys, and `SPACE`, while playing, pauses the game.
While paused, if `ESC` is pressed, the current game stops and the players goes back to the main menu.

There are four cheating options:
- **Invincibility (`V`)** - `pacman` doesn't collide with `ghosts`
- **Freeze (`F`)** - `ghosts` and `timers` stop.
- **Add Lives (`L`)** - The number of player lives is increased by one for every click
- **Skip Level (`N`)** - The current level ends and the player goes to the next.
