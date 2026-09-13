# Project Management — Pac-Man

*This project has been created as part of the 42 curriculum by fda-cruz, jsouza.*

## Overview


This document covers: team organization, task division, a timeline derived from git history, key technical decisions actually made, risk analysis, and a running record of blocking points and bugs as they're found.

Developed by a two person team over roughly three weeks.

## Team

| Member | Role |
|--------|------|
| Fábio Dias (`fda-cruz`) | Game Engine - Pacman, Ghosts, Level logic, Parser, Config, Highscore |
| João Souza (`jsouza`) | TODO |


## How We Worked

The project follows a strict **separation between game logic and rendering**: the engine side (`Game`, `Pacman`, `Ghost`, `Collectable`, `MazeAdapter`, `Highscore`, `parser`) has **no dependency on any graphics or input library**. `main.py` (owned by the UI side) is meant to instantiate `Game`, run the loop (read events → translate to abstract inputs → `game.update(...)` → render), and own everything Pygame/MLX-specific. This lets the engine be built and unit-tested headlessly, independently of the renderer's progress.

> TODO: describe actual day-to-day workflow (branching strategy, communication cadence, how decisions were made) once agreed with the teammate.

---

## Task Division

### Fabio — Game Engine
- `entities/entity.py`, `entities/pacman.py`, `entities/ghost.py`, `entities/collectable.py`
- `parser/parser.py`, `parser/utils.py` — configuration loading, comment stripping, validation
- `highscore/highscore.py` — persistent highscore system
- `manager/game.py` — game orchestration (state, score, lives, `update()`)
- Cheat mode flags

### Joao Souza — UI & Infrastructure
- Visual maze rendering, entity rendering, player animation
- Menus: main menu, instructions, pause menu, game over, highscore view
- GUI refactors (2026-09-11 / 2026-09-12)

> **Note, not smoothed over:** both `manager/game.py`'s log (Fabio) and the `front-end` branch (Joao) contain commits literally called "maze adapter" / "feat: maze adapter" on different dates (24, 27, 28 Aug). This means either (a) there are two different adapters — one for game logic, one for rendering — which is fine but should be named distinctly so it's obvious in the codebase which is which, or (b) there was duplicated/overlapping work that got merged without either of you noticing. Worth a 2-minute conversation with Joao to confirm which it is before writing this up as a final architecture decision — don't let the README's "General Software Architecture" section describe a single `MazeAdapter` if there are actually two.

---

## Timeline

Derived from `git log --all --pretty=format:'%ad | %an | %s' --date=short`, both branches in parallel.

| Date | Who | Milestone |
|---|---|---|
| 2026-08-24 | Both | Initial commits; `pyproject.toml`; UI init; `fabio` and `front-end` branches created |
| 2026-08-24 → 08-25 | Joao | Maze generator integration, first visual maze render, `.gitignore` cleanup, `draw_cell` refactor |
| 2026-08-26 | Fabio | Parser finished and tested |
| 2026-08-26 | Joao | Main menu screen |
| 2026-08-27 | Fabio | Extra parser tests, `Collectable` class |
| 2026-08-27 | Joao | Start-text blink, instructions menu; **PR #1** (`fabio → front-end`) merged |
| 2026-08-28 | Fabio | `MovableEntity`, `Pacman`, enums; `Entity`/`Collectable` updates; merged `main` into `fabio` |
| 2026-08-28 | Joao | Maze adapter (again — see note below); **PR #2** (`MazeAdapter → front-end`) merged |
| 2026-08-28 → 08-29 | Joao | Player + player animation |
| 2026-08-31 | Fabio | "Lots of progress and testing" |
| 2026-08-31 | Joao | Entity rendering |
| 2026-09-01 → 09-03 | Fabio | Ghost base class, ghost subclasses (untested), maze tests |
| 2026-09-07 → 09-08 | Joao | Base render, pause menu, game-over screen, highscore view; artifact cleanup; merges within `front-end` |
| 2026-09-09 → 09-10 | Fabio | "Game finished but not tested"; cheat options; highscore module |
| 2026-09-11 → 09-12 | Joao | GUI refactors |
| 2026-09-12 | Fabio | README started |
| 2026-09-12 | Fabio | Movement bug fixed (mid-move direction change teleporting through walls) and merged into `main` |

**Still not on `main` because it hasn't happened:** merging `front-end`. Everything Joao built from 09-07 onward exists only on `front-end` — see Blocking Points. (The `fabio` branch, including the movement fix above, is fully merged into `main` as of 2026-09-12.)

---

## Key Decisions

These are real design decisions already made and justified during development (see `pacman_design_notes.md`), not aspirational ones.

| Decision | Reason |
|---|---|
| `Game` has zero dependency on Pygame/MLX; `main.py` owns the loop and translates raw events into abstract inputs | Allows `Game.update()` to be built and unit-tested headlessly, in parallel with the UI side's progress |
| Ghost `EATEN` state resolved by a simple timer in `Game`, not by having the ghost walk back to a `home_position` | Simpler, decouples "being eaten" from pathfinding; the original walk-back approach was explored and explicitly discarded |
| `Ghost.update()` has a signature incompatible with `MovableEntity.update(delta, maze)` (needs `pacman_pos`, `pacman_direction`, `blinky_pos`) | Conscious LSP violation, accepted because `Game` never treats `Pacman` and `Ghost` polymorphically — it calls each type explicitly |
| `Ghost` keeps `self.maze` as a permanent attribute, unlike `Pacman` | `Ghost` is an autonomous state machine that must know the terrain to navigate every frame; `Pacman` never decides anything on its own, so it doesn't need it. Deliberate exception to the "pass everything as a parameter, never store" rule used for `pacman_pos`/`pacman_direction`/`blinky_pos` |
| `decide_direction()` runs **before** `super().update()` in `Ghost.update()` | If it ran after, a `next_direction` set this frame would only be consumed on the *next* alignment — the ghost would always react one step late, or keep going straight because `next_direction` would be `None` at the moment it was needed |
| `MazeAdapter.is_reachable(pos)` added specifically to exclude the central "42" block when picking random `FRIGHTENED` targets | The "42" pattern isn't a simple rectangle, so a bounding-box exclusion doesn't work; cells in that block are walled on all 4 sides, so `is_reachable` excludes them naturally |
| Ghost-vs-ghost collisions are never checked | Matches original Pac-Man behavior; visual overlap between ghosts is treated as a renderer concern, not a logic concern |
| `Highscore.add_score()` does not internally call `qualifies_highscore()` | Keeps `Highscore` a pure data/logic class with no opinion on *when* it should be called — that responsibility belongs to the caller (`main.py`), mirroring the `Game`/renderer separation |
| Faulty config values are corrected field-by-field, not file-by-file | A single invalid key must not discard an otherwise valid config, per subject `V.3` |

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| A-Maze-ing package (external, unmodifiable) has an interface or output that doesn't match our assumptions | Medium | High | `MazeAdapter` isolates the rest of the codebase from the external package's API; defensive checks (`is_walkable` checks walls on both sides of a boundary) rather than trusting mutual consistency |
| Graphics library choice not yet made / no contract agreed with the UI teammate | High (currently true) | High | Tracked as an open blocking point (see below); engine built to be UI-agnostic specifically to reduce the cost of this being late |
| Deliberate LSP violation (`Pacman`/`Ghost` incompatible `update()` signatures) causes confusion or misuse from the UI side | Low | Medium | Documented explicitly in design notes and to be documented again in the README's architecture section |
| Cheat-mode toggle keys implemented with `get_pressed()` instead of a one-shot `KEYDOWN` event, causing rapid ON/OFF flicker | Medium (identified, not yet fixed) | Medium | Documented as a known pitfall to avoid in `main.py`; must be handled once input code exists |
| No packaging/build script exists yet, subject requires a deployable public-platform build | High (currently true) | High | Tracked as an open blocking point |

---

## Acceptance Test Plan

> Based on the subject's mandatory features. Test steps assume `main.py` and the renderer exist; several rows are currently untestable end-to-end and are marked accordingly.

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

---

## Blocking Points

| Issue | Status | Notes |
|---|---|---|
| No graphics library chosen yet (MLX or MLX-equivalent) | Open | Must be agreed with the UI teammate before `main.py`/renderer work starts; subject requires any library used to have a 1:1 function equivalent with MLX |
| Exact `Game` ↔ renderer/input contract not agreed | Open | Needs a decision on what the renderer receives from `Game` and who owns input translation |
| Cheat-mode toggle keys must be one-shot (`KEYDOWN`), not `get_pressed()` | Identified, not yet implemented | Flagged explicitly to avoid ON/OFF flicker while a key is held; applies to `invincible`/`ghost_freeze` toggles and to one-shot actions like `skip_level()`/`add_lives()` |
| Speed cheat needs `self.speed` on `MovableEntity`, which doesn't exist yet | Open | Currently blocks implementing the "increased speed" cheat feature from `VI.5` |
| `self.collectables` was declared as `dict[tuple[int, int], Collectable]` (a generic alias, not an actual dict) | Fixed | Corrected to populate an empty `{}` in `setup_level()`, consistent with other attributes |
| `Highscore` implemented and tested in isolation but not wired into `Game`/`main.py` | Open | Need to decide who calls `qualifies_highscore()` → prompts for name → `add_score()` → `save_highscore()`, and when |
| No packaging script/spec exists | Open | Subject `VII` requires the packaging script/spec at the repository root and a build deployable to a public platform |
| `front-end` branch (all UI/rendering work, including everything from 2026-09-07 onward) never merged into `main` | **Open, active as of 2026-09-12** | Confirmed via `git log --oneline main..front-end`: dozens of unmerged commits. `main` currently has no GUI at all. Must check for conflicts (`git merge --no-commit --no-ff front-end` on a disposable branch first) before merging for real |
| Possible duplicated "maze adapter" work between Fabio's and Joao's branches | Open, unconfirmed | Both branches have commits named "maze adapter" on different dates; needs a direct conversation to confirm whether these are legitimately two different components or accidental overlap |
| Player can teleport through walls when a new direction is pressed before the current move animation finishes | **Fixed (2026-09-12)** | Reported symptom: pressing a new direction mid-movement let the animation for the *old* direction finish while the logical position ended up in the *new* direction. Root cause: `MovableEntity.update()` finalized the move with `self.get_next_position()`, which reads `self.next_direction` when set — so completing a move silently applied an **unvalidated** direction change, bypassing `maze.is_walkable()` entirely for that step. Fix: finalize the move with `self.get_next_position_on(self.pos, self.direction)` instead, which always closes the move in the direction that was actually validated and animated. `next_direction` is still applied, but only on the next cycle (`move_progress <= 0.0`), where it goes through `is_walkable` normally. |

---

## Testing Strategy

Two categories of testing exist today, and they are **not the same thing** — kept distinct here on purpose rather than presented as equivalent.

### 1. Manual verification scripts (exist today)

These generate real output for human inspection. They have no `assert` and no pass/fail signal — a human decides whether the result is correct by reading it.

| Script | Purpose | Coverage |
|---|---|---|
| `tests/test_parser.py` + `test_parser.sh` | Exercises `parser_configuration_file` against a JSON config for every case the subject requires: fully valid config, missing keys, invalid types, out-of-range values, unknown keys, malformed JSON | Input space: exhaustive, by design. All documented `V.2`/`V.3` cases have a corresponding generated config file. |
| `tests/test_maze.py` + `test_maze.sh` | Renders the maze to the terminal (ASCII, colour-coded) for a given width/height/seed | Was used to determine, by direct visual inspection, where Pacman's spawn cell should be relative to the generated grid — a discovery tool, not a regression check |

**Value:** the parser input coverage is genuinely complete for known cases — that part of the work is solid. The maze script served its purpose (finding the spawn rule) and remains useful as an ad-hoc debugging tool whenever the `MazeAdapter`'s output needs to be eyeballed again.

**Limit:** neither script can fail loudly. If the parser's clamping logic regresses, or the spawn-cell rule breaks after a `MazeAdapter` change, these scripts will keep printing output — nothing will flag that the output is now *wrong* unless a human re-reads it and remembers what "right" looked like.

### 2. Automated tests (not yet written)

No `pytest`/`unittest` file exists in the project yet. This is a known gap, not an oversight being ignored — see Open Points.

Highest-value first candidate, precisely because it already caused a real bug (see Blocking Points, "Player can teleport through walls"): a test that drives `MovableEntity.update()` directly — set a direction, advance `move_progress` partway, buffer a `next_direction` mid-move, advance until the move completes, and assert the final `self.pos` matches the *validated* direction, not the buffered one. This single test would have caught the teleport bug before João did, and would catch any regression of the fix applied on 2026-09-12.

---

## Open Points (not yet decisions)

- Graphics library selection (see Blocking Points).
- Real project timeline, once actual work dates are available.
- Whether `main.py`'s two `try/except ValueError` points (initial `Game` creation and the main loop, both possible sources of an uncaught `ValueError` from the Pacman fallback in `setup_level()`) are implemented — required by subject `V.1` to avoid a traceback ever reaching the terminal.
- **Automated testing with `pytest`/`unittest`**: wanted, not yet done, and not yet known-how by the team. Starting point agreed: begin with the movement/direction-change case (see Testing Strategy), since it's small, self-contained, and already known to matter.
