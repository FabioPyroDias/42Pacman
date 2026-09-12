"""
Game manager for Pac-Man.

Handles game initialization, level state management, score tracking
and collisions across game loops.
"""

from typing import Any
from maze.maze_adapter import MazeAdapter
from entities.pacman import Pacman
from entities.ghost import Ghost, Blinky, Pinky, Inky, Clyde
from entities.collectable import Collectable, Pacgum, SuperPacgum
from enums import Direction, GhostState, GameState
from consts import (WAVE_TIMERS_SCATTER_CHASE, TIMER_FRIGHTENED, TIMER_EATEN,
                    TIMER_RESPAWN)
from random import randint


class Game():
    """
    Main controller for game state, maze layout, and entity interactions.

    Attributes:
        config (dict[str, Any]): Global game parameters preserved for
            subsequent levels.
        score (int): Cumulative player score.
        lives (int): Remaining lives.
        current_level_index (int): Active level index.
        maze (MazeAdapter): Grid adapter instantiated during level setup.
        pacman (Pacman): Player character instance.
        ghosts (list[Ghost]): Active ghost entities.
        collectables (dict[tuple[int, int], Collectable]): Map of grid
            coordinates to Pacgum and SuperPacgum.
        level_timer (float): Total elapsed time in the active level.
        respawn_timer (float): Time delay during death sequence before
            resetting entities.
        scatter_chase_timer (float): Timer that alternates
            global ghost states (Scatter/Chase).
        frightened_timer (float): Active timer for Ghosts frightened state.
        eaten_timer (dict[Ghost, float]): Respawn duration trackers per
            eaten ghost.
        game_state (GameState): Active global game state.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initializes game state, entities setup, and ghost mode timers.

        Args:
            config (dict[str, Any]): Configuration dictionary containing
                initial settings.

        Returns:
            None
        """

        self.config = config
        self.score = 0
        self.lives = config["lives"]
        self.current_level_index = 0

        self.maze: MazeAdapter
        self.pacman: Pacman
        self.ghosts: list[Ghost]
        self.collectables: dict[tuple[int, int], Collectable]

        self.level_timer = 0.0

        self.respawn_timer = 0.0

        self.wave_index = 0
        self.ghost_state = GhostState.SCATTER

        self.scatter_chase_timer = 0.0
        self.frightened_timer = 0.0
        self.eaten_timer: dict[Ghost, float]

        self.generate_maze()
        self.setup_level()

        self.cheat_invincible = False
        self.cheat_ghost_freeze = False

    def setup_level(self) -> None:
        """
        Initializes level layout, entities, collectables, and timers.

        Loads level parameters from configuration, generates the maze grid,
        populates Pacgums and SuperPacgums, positions Paman and the four ghosts
        with their respective scatter zones, and resets all game timers.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError
        """

        if self.current_level_index >= len(self.config["level"]):
            self.game_state = GameState.VICTORY
            return

        configs = self.config["level"][self.current_level_index]

        # Pacgums and SuperPacgums Section
        self.collectables = {}

        for row in range(configs["height"]):
            for col in range(configs["width"]):
                if ((row == 0 and col == 0)
                   or (row == configs["height"] - 1 and col == 0)
                   or (row == 0 and col == configs["width"] - 1)
                   or (row == configs["height"] - 1
                        and col == configs["width"] - 1)):
                    self.collectables[(col, row)] = (
                        SuperPacgum((col, row),
                                    self.config["points_per_super_pacgum"]))
                elif self.maze.is_reachable((col, row)):
                    self.collectables[(col, row)] = (
                        Pacgum((col, row),
                               self.config["points_per_pacgum"]))

        # Pacman Section
        self.reset_pacman()

        # Ghosts Section
        self.reset_ghosts()

        # Reset timers
        self.level_timer = 0.0
        self.reset_timers()

        self.wave_index = 0
        self.ghost_state = GhostState.SCATTER

        self.game_state = GameState.PLAYING

    def check_collisions(self,
                         pacman_previous_position: tuple[int, int],
                         ghosts_previous_position: dict[Ghost,
                                                        tuple[int, int]]
                         ) -> bool:
        """
        Checks collisions between Pacman and ghosts or collectables.

        Args:
            pacman_previous_position (tuple[int, int]): Pacman position
                before update.
            ghosts_previous_position (dict[Ghost, tuple[int, int]]): Ghost
                positions before update.

        Returns:
            bool: True if Pacman collided with a ghost. False otherwise.
        """

        # Check collisions between Pacman and Ghosts
        for ghost in self.ghosts:
            if ghost.state == GhostState.EATEN:
                continue

            direct_collision = ghost.pos == self.pacman.pos
            swap_collision = (
                self.pacman.pos == ghosts_previous_position[ghost]
                and pacman_previous_position == ghost.pos
            )

            if direct_collision or swap_collision:
                if ghost.state == GhostState.FRIGHTENED:
                    ghost.state = GhostState.EATEN
                    self.score += self.config["points_per_ghost"]
                    self.eaten_timer[ghost] = 0.0
                else:
                    # If invincible, collision didn't happen
                    if not self.cheat_invincible:
                        self.lives -= 1
                        return True

        # Check collisions between Pacman and Pacgums
        collectable = self.collectables.pop(self.pacman.pos, None)
        if collectable:
            collectable_info = collectable.on_collected()
            self.score += int(collectable_info["points"])
            if collectable_info.get("effect", None):
                for ghost in self.ghosts:
                    if ghost.state == GhostState.EATEN:
                        continue
                    ghost.state = GhostState.FRIGHTENED

                self.frightened_timer = 0.0

        return False

    def check_level_complete(self) -> None:
        """
        Updates game_state to LEVEL_COMPLETE if all maze collectables
            have been eaten.

        Args:
            None

        Returns:
            None
        """

        if not self.collectables:
            self.game_state = GameState.LEVEL_COMPLETE

    def check_game_over(self) -> None:
        """
        Updates game_state to GAME_OVER when remaining lives reach zero.
        If they haven't, reset positions of Pacman, Ghosts and timers, also
            updating game_state to RESPAWNING.

        Args:
            None

        Returns:
            None
        """

        if self.lives == 0:
            self.game_state = GameState.GAME_OVER
        else:
            self.reset_pacman()
            self.reset_ghosts()
            self.reset_timers()
            self.game_state = GameState.RESPAWNING

    def update(self, delta: float) -> None:

        if self.game_state == GameState.RESPAWNING:
            self.respawn_timer += delta
            if self.respawn_timer >= TIMER_RESPAWN:
                self.respawn_timer = 0.0
                self.game_state = GameState.PLAYING
            return

        if self.game_state == GameState.PAUSED:
            return

        if self.game_state == GameState.LEVEL_COMPLETE:
            self.current_level_index += 1
            self.generate_maze()
            self.setup_level()
            return

        if self.game_state == GameState.VICTORY:
            return

        if not self.cheat_ghost_freeze:
            self.update_timers(delta)

        if self.game_state == GameState.RESTART_LEVEL:
            self.lives -= 1
            if self.lives == 0:
                self.game_state = GameState.GAME_OVER
            else:
                self.setup_level()
            return

        previous_pos_pacman = self.pacman.pos
        self.pacman.update(delta, self.maze)

        previous_pos_ghosts = {}
        for ghost in self.ghosts:
            previous_pos_ghosts[ghost] = ghost.pos
            if not self.cheat_ghost_freeze:
                ghost.update_ghost(delta, self.pacman.pos,
                                   self.pacman.direction,
                                   self.ghosts[0].pos)

        if self.check_collisions(previous_pos_pacman, previous_pos_ghosts):
            self.check_game_over()
        else:
            self.check_level_complete()

    def set_player_direction(self, next_direction: Direction) -> None:
        """
        Sets the next movement direction for Pacman.

        Args:
            next_direction (Direction): Target direction to apply on
                Pacman's next valid turn.

        Returns:
            None
        """

        self.pacman.set_next_direction(next_direction)

    def reset_pacman(self) -> None:
        """Resets Pacman to its default starting position and direction.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError
        """

        configs = self.config["level"][self.current_level_index]

        pacman_pos_x = 0
        if configs["width"] % 2 == 0:
            pacman_pos_x = configs["width"] // 2 - 1
        else:
            pacman_pos_x = configs["width"] // 2

        pacman_pos_y = 0
        if configs["height"] % 2 == 0:
            pacman_pos_y = configs["height"] // 2 + 1
        else:
            pacman_pos_y = configs["height"] // 2 + 2

        # In case the "42" pattern is different from expected, pacman spawn
        #   position lowers one cell for each iteration while still
        #   within maze boundaries
        while (not self.maze.is_reachable((pacman_pos_x, pacman_pos_y))
                and pacman_pos_y < configs["height"] - 1):
            pacman_pos_y += 1

        # If the pacman spawn position isn't valid, an error is raised.
        # The pattern should work, but the maze might be invalid. Not the
        #   group's fault
        if not self.maze.is_reachable((pacman_pos_x, pacman_pos_y)):
            raise ValueError(f"Could not find a walkable spawn cell "
                             f"for Pacman in level "
                             f"{self.current_level_index}. "
                             f"Maze is invalid.")

        self.pacman = Pacman((pacman_pos_x, pacman_pos_y), Direction.NORTH)

    def reset_ghosts(self) -> None:
        """Reinstantiates all ghosts at their initial spawn points and states.

        Positions Blinky, Pinky, Inky, and Clyde in their designated
            maze corners facing NORTH, resetting their current state to
            SCATTER and recalculating their corner scatter zones.

        Args:
            None

        Returns:
            None
        """

        configs = self.config["level"][self.current_level_index]

        blinky_pos = (0, 0)
        pinky_pos = (configs["width"] - 1, 0)
        inky_pos = (0, configs["height"] - 1)
        clyde_pos = (configs["width"] - 1, configs["height"] - 1)

        size_percentage = 0.2

        blinky_scatter_top_left = (0, 0)
        blinky_scatter_bottom_right = (
            int(configs["width"] * size_percentage),
            int(configs["height"] * size_percentage))

        pinky_scatter_top_left = (
            (configs["width"] - 1) - int(configs["width"] * size_percentage),
            0)
        pinky_scatter_bottom_right = (
            configs["width"] - 1,
            int(configs["height"] * size_percentage))

        inky_scatter_top_left = (
            0,
            (configs["height"] - 1) - int(configs["height"] * size_percentage)
            )
        inky_scatter_bottom_right = (
            int(configs["width"] * size_percentage), configs["height"] - 1)

        clyde_scatter_top_left = (
            (configs["width"] - 1) - int(configs["width"] * size_percentage),
            (configs["height"] - 1) - int(configs["height"] * size_percentage)
            )
        clyde_scatter_bottom_right = (
            configs["width"] - 1, configs["height"] - 1)

        self.ghosts = [
            Blinky(blinky_pos, Direction.NORTH, self.maze, GhostState.SCATTER,
                   blinky_scatter_top_left, blinky_scatter_bottom_right),
            Pinky(pinky_pos, Direction.NORTH, self.maze, GhostState.SCATTER,
                  pinky_scatter_top_left, pinky_scatter_bottom_right),
            Inky(inky_pos, Direction.NORTH, self.maze, GhostState.SCATTER,
                 inky_scatter_top_left, inky_scatter_bottom_right),
            Clyde(clyde_pos, Direction.NORTH, self.maze, GhostState.SCATTER,
                  clyde_scatter_top_left, clyde_scatter_bottom_right),
        ]

    def reset_timers(self) -> None:
        """
        Resets timers

        Args:
            None

        Returns:
            None
        """
        self.scatter_chase_timer = 0.0
        self.frightened_timer = 0.0
        self.eaten_timer = {}

    def update_timers(self, delta: float) -> None:
        self.level_timer += delta
        if self.level_timer >= self.config["level_max_time"]:
            self.game_state = GameState.RESTART_LEVEL
            return

        is_ghost_in_frightened = False
        for ghost in self.ghosts:
            if ghost.state == GhostState.FRIGHTENED:
                is_ghost_in_frightened = True
                break

        if not is_ghost_in_frightened:
            if self.wave_index < len(WAVE_TIMERS_SCATTER_CHASE):
                self.scatter_chase_timer += delta
                timer_scatter, timer_chase = (
                    WAVE_TIMERS_SCATTER_CHASE[self.wave_index])

                if (self.ghost_state == GhostState.SCATTER
                   and self.scatter_chase_timer >= timer_scatter):
                    self.ghost_state = GhostState.CHASE
                    self.scatter_chase_timer = 0.0
                    for ghost in self.ghosts:
                        if ghost.state != GhostState.EATEN:
                            ghost.state = self.ghost_state
                elif (self.ghost_state == GhostState.CHASE
                      and self.scatter_chase_timer >= timer_chase):
                    self.wave_index += 1
                    if self.wave_index < len(WAVE_TIMERS_SCATTER_CHASE):
                        self.ghost_state = GhostState.SCATTER
                        self.scatter_chase_timer = 0.0
                        for ghost in self.ghosts:
                            if ghost.state != GhostState.EATEN:
                                ghost.state = self.ghost_state

        else:
            self.frightened_timer += delta
            if self.frightened_timer >= TIMER_FRIGHTENED:
                self.frightened_timer = 0.0
                for ghost in self.ghosts:
                    if ghost.state != GhostState.EATEN:
                        ghost.state = self.ghost_state

        for ghost in self.ghosts:
            if ghost.state == GhostState.EATEN:
                self.eaten_timer[ghost] += delta
                if self.eaten_timer[ghost] >= TIMER_EATEN:
                    self.eaten_timer.pop(ghost)
                    ghost.state = self.ghost_state

    def generate_maze(self) -> None:
        configs = self.config["level"][self.current_level_index]
        chosen_seed = 0
        if self.current_level_index == 0:
            chosen_seed = self.config["seed"]
        else:
            chosen_seed = randint(0, 2 ** 31 - 1)

        self.maze = MazeAdapter((configs["width"], configs["height"]),
                                chosen_seed)

    def toggle_pause(self) -> None:
        if self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING
        elif self.game_state == GameState.PLAYING:
            self.game_state = GameState.PAUSED

    def cheat_toggle_invincible(self) -> None:
        self.cheat_invincible = not self.cheat_invincible

    def cheat_toggle_ghost_freeze(self) -> None:
        self.cheat_ghost_freeze = not self.cheat_ghost_freeze

    def cheat_skip_level(self) -> None:
        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.LEVEL_COMPLETE

    def cheat_add_lives(self) -> None:
        self.lives += 1
