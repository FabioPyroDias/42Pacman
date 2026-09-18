*This project has been created as part of the 42 curriculum by fda-cruz, jsouza.*

# Project Management - Pac-Man

## Overview

This document covers: team organization, task division, a timeline derived from git history, key technical decisions actually made, risk analysis, and a running record of blocking points and bugs as they're found.

Developed by a two person team over roughly three weeks.

## Team

| Member | Role |
|--------|------|
| Fábio Dias (`fda-cruz`) | Game Engine - Pacman, Ghosts, Level logic, Parser, Config, Highscore |
| João Souza (`jsouza`) | UI Engine - Rendering, Menus, Animation, Input Handling (`pac-man.py`) |

## How We Worked

The project follows a strict separation between game logic and rendering. The engine side where `Game`, `Pacman`, `Ghost`, `Collectable`, `MazeAdapter`, `Highscore`, `parser` exist, has no dependency on any graphics or input library. `pac-man.py` (owned by the UI side) is meant to instantiate `Game`, run the loop (read events → translate to abstract inputs → `game.update(...)` → render), and own everything Pygame/MLX-specific. This lets the engine be built and unit-tested headlessly, independently of the renderer's progress.

We worked almost daily in a remote environment with occassional meetings, sharing updates, design decisions and concept sharing. This allowed for a free, non pressure development process but still rigorous.

Using different branches on Github, we were able to focus on each task, allowing for a cleaner organization and more stable main branch.

By the end of the project, several questions were made on how to improve the game, as well as fixing some bugs and having some in-depth explanation of approaches to each task.


## Task Division

### Fabio - Game Engine
- `entities/entity.py`, `entities/pacman.py`, `entities/ghost.py`, `entities/collectable.py`
- `parser/parser.py`, `parser/utils.py` - configuration loading, comment stripping, validation
- `highscore/highscore.py` - persistent highscore system
- `manager/game.py` - game orchestration (state, score, lives, `update()`)
- Cheat mode flags

### Joao Souza - UI & Infrastructure

`ui/gui.py` is the sole owner of the window/surface and runs the render loop; game logic never touches `pygame.display` directly. Rendering follows the State Pattern — each screen under `ui/states/*.py` (`main_menu`, `gameplay`, `pause_menu`, `game_over`, `victory`, `highscore_view`, `instructions`) exposes only a `render(surface, game_state)` method, with no input handling or logic of its own. Entity rendering uses one XPM spritesheet per entity (directions as rows, animation frames as columns), animated at 12fps decoupled from the main loop via `time.perf_counter()`. Also responsible for validating every new UI-side pygame feature against the MLX-equivalence constraint before use.

- Visual maze rendering, entity rendering, player animation
- Menus: main menu, instructions, pause menu, game over, highscore view
- GUI refactors (2026-09-11 / 2026-09-12)

## Timeline

| Date | Who | Milestone |
|------|-----|-----------|
| 2026-08-24 | Both | Initial commits, `pyproject.toml`, UI init, different branches created |
| 2026-08-24 -- 08-25 | João | Maze generator integration, first visual maze render, `.gitignore` cleanup, `draw_cell` refactor |
| 2026-08-26 | Fabio | Parser finished and tested |
| 2026-08-26 | João | Main menu screen |
| 2026-08-27 | Fabio | Extra parser tests, `Collectable` class |
| 2026-08-27 | João | Start-text blink, instructions menu |
| 2026-08-28 | Fabio | `MovableEntity`, `Pacman`, enums, `Entity`/`Collectable` updates |
| 2026-08-28 | João | Update Maze adapter |
| 2026-08-28 -- 08-29 | João | Player and player animation |
| 2026-08-31 | Fabio | Several tests, `Entity`, `MovableEntity` and `Pacman` cleanup |
| 2026-08-31 | João | Entity rendering |
| 2026-09-01 -- 09-03 | Fabio | Ghost base class, ghost subclasses, maze tests |
| 2026-09-07 -- 09-08 | João | Base render, pause menu, game-over screen, highscore view, artifact cleanup |
| 2026-09-09 | Fabio | `Game` finished (not yet tested) |
| 2026-09-10 | Fabio | Cheat options, highscore module |
| 2026-09-11 -- 09-12 | João | GUI refactors |
| 2026-09-12 | Fabio | README started; movement bug fixed |
| 2026-09-13 | Fabio | Collision bug fix, follow-up quick fix |
| 2026-09-13 | João | mypy fixes; Pacman moonwalk (direction-reversal) bug addressed |
| 2026-09-14 | Fabio | `project_management/` doc added; full pass of comments/docstrings on `main` |
| 2026-09-14 | João | Name-entry screen implemented |
| 2026-09-15 | João | Bug fixes; added READY (countdown) scene |
| 2026-09-16 | João | Bug fixes |
| 2026-09-17 | João | Merged `fabio` branch into `front-end`; module docstrings added across game/scene/package/entrypoint modules (including a Copilot-assisted PR) |
| 2026-09-18 | João | Additional docstrings added |

**Still not on `main`:** the `front-end` branch (all UI work from 09-07 onward, including everything above) has not yet been merged — see Blocking Points.

## Key Decisions

| Decision | Reason |
|----------|--------|
| `Game` has zero dependency on #!Atenção!# ####JOAO -> Motor gráfico?; `main.py` owns the loop and translates raw events into abstract inputs | Allows `Game.update()` to be built and unit-tested headlessly, in parallel with the UI side's progress |
| Ghost `EATEN` state resolved by a simple timer in `Game`, not by having the ghost walk back to a `home_position` | Simpler, decouples "being eaten" from pathfinding, the original walk-back approach was explored and explicitly discarded |
| `Ghost.update()` has a signature incompatible with `MovableEntity.update(delta, maze)`, where it needs `pacman_pos`, `pacman_direction`, `blinky_pos` | Conscious decision, accepted because `Game` never treats `Pacman` and `Ghost` polymorphically |
| `Ghost` keeps `self.maze` as a permanent attribute, unlike `Pacman` | `Ghost` is an autonomous state machine that must know the terrain to navigate every frame. `Pacman` never decides anything on its own, so it doesn't need it. Deliberate exception to the "pass everything as a parameter, never store" rule used for `pacman_pos`, `pacman_direction`, `blinky_pos` |
| `decide_direction()` runs before `super().update()` in `Ghost.update()` | If it ran after, a `next_direction` set this frame would only be consumed on the next alignment. This would mean the ghost would always react one step late, or keep going straight because `next_direction` would be `None` at the moment it was needed |
| `MazeAdapter.is_reachable(pos)` added specifically to exclude the central "42" block when picking random `FRIGHTENED` targets | The "42" pattern isn't a simple rectangle, so a bounding box exclusion doesn't work, cells in that block are walled on all 4 sides, so `is_reachable` excludes them naturally |
| Ghost vs Ghost collisions are never checked | Matches original Pac-Man behavior. Visual overlap between ghosts is treated as a renderer concern, not a logic concern |
| `Highscore.add_score()` does not internally call `qualifies_highscore()` | Keeps `Highscore` a pure data class with no opinion on when it should be called. This responsibility belongs to the caller, `main.py`, mirroring the `Game` and renderer separation |
| Faulty config values are corrected field by field instead of the whole file | A single invalid key must not discard an otherwise valid config |

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| The external A-Maze-ing package has an interface or output that doesn't match our assumptions | Medium | High | `MazeAdapter` isolates the rest of the codebase from the external package's API. Defensive checks such as `is_walkable` checks walls on both sides of a boundary are implemented rather than trusting mutual consistency |
##### JOÃO! TODO
| Graphics library choice not yet made / no contract agreed with the UI teammate | High (currently true) | High | Tracked as an open blocking point (see below); engine built to be UI-agnostic specifically to reduce the cost of this being late |
| Deliberate `update()` incompatible signature mismatch between `Pacman` and `Ghost` causes confusion or misuse from the UI side | Low | Medium | Explicitly discussed between teammates |
#### JÕAO -> TODO!
| Cheat mode toggle keys implemented with `get_pressed()` instead of a one-shot `KEYDOWN` event, causing rapid ON/OFF flicker | Medium (identified, not yet fixed) | Medium | Documented as a known pitfall to avoid in `main.py`; must be handled once input code exists |

### TODO -> GERAL
| No packaging/build script exists yet, subject requires a deployable public-platform build | High (currently true) | High | Tracked as an open blocking point |

## Acceptance Test Plan


### JOÃO -> TALVEZ SEJA MELHOR OLHARES TU PARA ESTA TABELA.
| Feature | How to test | Expected result | Status |
|---|---|---|---|
| Config parsing with comments | Launch with a config containing `#`/`//` lines and an invalid field | Comments ignored, invalid field replaced by default, no traceback | Testable now (headless) |
| Maze generation (level 1, fixed seed) | Launch game twice with same seed | Identical maze both times | Testable now (headless) |
| Maze generation (level > 1) | Complete level 1 | New, different maze generated | Testable now (headless) |
| Player movement | Arrow keys / WASD | Player moves through corridors, blocked by walls | Blocked — needs `main.py`/input |
| Pacgum collection | Walk over dot | Score `+points_per_pacgum`, dot removed | Testable now (headless, via `Game.update`) |
| Super-pacgum | Walk over corner dot | Score `+points_per_super_pacgum`, ghosts become edible | Testable now (headless) |
| Eat edible ghost | Touch frightened ghost | Score `+points_per_ghost`, ghost respawns after delay | Testable now (headless) |
| Lose life | Touch non-edible ghost | Life count decreases, player respawns center | Testable now (headless) |
| Game over | Lose all lives | Game over state reached | Testable now (headless) |
| Win level / win game | Eat all pacgums / complete all levels | Level/game win state reached | Testable now (headless) |
| Highscore save/load | Qualifying score at game end | Name entry, saved, appears in top 10 | Partially testable — `Highscore` alone works, not wired to `Game` yet |
| Cheat mode (all flags) | Toggle each flag | Invincibility / ghost freeze / level skip / extra lives behave as documented | Blocked — needs `main.py` key bindings |
| Pause/resume | Pause during play | Game freezes, resumes correctly | Blocked — needs `main.py`/renderer |
| Packaging | Run packaging script | Runnable build produced | Blocked — no script exists yet |

## Blocking Points

| Issue | Solution |
|-------|-------|
| `Pacman` can teleport through walls when a new direction is pressed before the current move animation finishes | Finalize the move with `self.get_next_position_on(self.pos, self.direction)` instead. This always closes the move in the direction that was actually validated and animated. `next_direction` is still applied, but only on the next cycle, when `move_progress <= 0.0`, where it goes through `is_walkable` normally |
| Collision between `Pacman` and `Ghost` when both entities are far away | The `Ghost` visual position did not match the logical position. Solved by applying the true position to the rendered `Ghost` |
| Crash when having different keys in `config.json` | Fixed with a simple `get()` |

## Testing Strategy

### 1. Manual verification scripts

| Script | Purpose |
|--------|---------|
| `tests/test_parser.py` and `test_parser.sh` | Exercises `parser_configuration_file` against a JSON config for every case the subject requires: fully valid config, missing keys, invalid types, out of range values, unknown keys, malformed JSON |
| `tests/test_maze.py` and `test_maze.sh` | Renders the maze to the terminal for a given width, height and seed. Was used to determine, by direct visual inspection and analysis, where `Pacman's` spawn cell should be relative to the generated maze |

#### TODO -> -> VAI SER PRECISO CRIAR PYTESTS.
### 2. Automated tests (not yet written)

No `pytest`/`unittest` file exists in the project yet. This is a known gap, not an oversight being ignored — see Open Points.
