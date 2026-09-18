"""Gameplay scene rendering and animations."""

import pygame
from time import perf_counter
from enums import Direction, GhostState, GameState
from entities import Ghost, SuperPacgum, Pacgum
from manager.game import Game
from maze import Cell, MazeAdapter
from .base_render import BaseRender
from consts import (
    CELL_SIZE, WALL_OFFSET, SPRITE_SIZE, WALL_THICKNESS,
    WALL_COLOR, BACKGROUND_COLOR, PACMAN_SPRITE_LAST_INDEX_X,
    PACMAN_DEATH_SPRITE_LAST_INDEX_Y, PACMAN_DEATH_SPRITE_START_INDEX_Y,
    GHOST_SPRITE_LAST_INDEX_X, ENTITIES_DOWN_SPRITE_INDEX_Y,
    ENTITIES_LEFT_SPRITE_INDEX_Y, ENTITIES_RIGHT_SPRITE_INDEX_Y,
    ENTITIES_UP_SPRITE_INDEX_Y, PACMAN_SPRITE_PATH, PACGUM_SPRITE_PATH,
    SUPER_PACGUM_SPRITE_PATH, BLINKY_SPRITE_PATH, PINKY_SPRITE_PATH,
    INKY_SPRITE_PATH, CLYDE_SPRITE_PATH, FT_BACKGROUND_COLOR,
    DEAD_GHOST_SPRITE_LAST_INDEX_X, TIMER_FRIGHTENED,
    FLASHING_GHOST_SPRITE_INDEX_Y, SCARED_GHOST_SPRITE_INDEX_Y,
    DEATH_FREEZE_DURATION
    )


Coordinates = tuple[int, int]


class Gameplay(BaseRender):
    """
    Gameplay class for rendering the game state in a graphical interface.

    This class extends the BaseRender class and is responsible for loading
    assets,
    updating the game state, and rendering the game elements such as Pacman,
    ghosts,
    and the maze.

    Attributes:
        __assets_loaded (bool): Indicates whether the game assets have been
        loaded.
        __updated (bool): Indicates whether the game state has been updated.
        __flashing (bool): Indicates whether the ghosts are in a flashing
        state.
        __wait (bool): Indicates whether the game is in a wait state.
        __wait_timer (float): Timer for managing wait durations.
        __last_flash (float): Timestamp of the last flash event for ghosts.
        __pacman_sprite_index_x (int): Current sprite index for Pacman's
        animation in the x-direction.
        __pacman_sprite_index_y (int): Current sprite index for Pacman's
        animation in the y-direction.
        __pacman_dead_sprite_index_x (int): Current sprite index for Pacman's
        death animation in the x-direction.
        __pacman_dead_sprite_index_y (int): Current sprite index for Pacman's
        death animation in the y-direction.
        __pacman_last_state (GameState): Last known state of Pacman.
        __sprites_y (dict): Dictionary mapping ghost IDs to their
        y-coordinates.
        __sprites_x (dict): Dictionary mapping ghost IDs to their
        x-coordinates.
        __last_ghost_state (dict): Dictionary mapping ghost IDs to their last
        known states.
        _background (pygame.Surface | None): Background surface for rendering.
        __last_pacman_frame_time (float): Timestamp of the last frame rendered
        for Pacman.
        __last_frame_time (dict): Dictionary mapping ghost IDs to their last
        frame render timestamps.

    Methods:
        __load_assets(): Loads the necessary game assets for rendering.
        __update(maze: MazeAdapter): Updates the game state and window size
        based on the current maze.
        _draw_cell(cell: Cell, coord: Coordinates): Draws a single cell of the
        maze.
        _render_map(): Renders the entire maze.
        _render_pacman(game_state: GameState, stop: bool): Renders the Pacman
        character based on the game state.
        _render_ghosts(frightened_timer: float, stop: bool): Renders the
        ghosts, handling their states and animations.
        _render_pacgums(): Renders the Pacgums in the maze.
        _render_scared_ghost(sprite: pygame.Surface, ghost: Ghost,
        last_index_x: int, stop: bool): Renders a scared ghost.
        _render_ghost(sprite: pygame.Surface, ghost: Ghost, last_index_x: int,
        stop: bool): Renders a ghost.
        _render_pacman_entity(sprite: pygame.Surface, last_index_x: int,
        stop: bool): Renders the Pacman entity.
        _render_pacman_death(sprite: pygame.Surface, last_index_x: int,
        last_index_y: int, start_index_y: int, stop: bool): Renders Pacman's
        death animation.
        render_gameplay(frightened_timer: float, game_state: GameState,
        maze: MazeAdapter, stop: bool = False): Main method to render the
        gameplay, updating the state and rendering all elements.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initialize the game renderer with the specified window size,
        title, game instance, and maze adapter.

        Args:
            win_size (tuple[int, int]): The size of the game window as a
            tuple of (width, height).
            title (str): The title of the game window.
            game (Game): An instance of the Game class representing the
            current game state.
            maze (MazeAdapter): An adapter for the maze structure used in
            the game.

        Returns:
            None
        """
        super().__init__(win_size, title, game, maze)
        self.__assets_loaded = False
        self.__updated = False
        self.__flashing = False
        self.__wait = False
        self.__wait_timer = 0.0
        self.__last_flash = 0.0
        self.__pacman_sprite_index_x = 0
        self.__pacman_sprite_index_y = 0
        self.__pacman_dead_sprite_index_x = 0
        self.__pacman_dead_sprite_index_y = PACMAN_DEATH_SPRITE_START_INDEX_Y
        self.__pacman_last_state = GameState.PLAYING
        self.__sprites_y = {ghost.id: 0 for ghost in self._game.ghosts}
        self.__sprites_x = {ghost.id: 0 for ghost in self._game.ghosts}
        self.__last_ghost_state = {ghost.id: ghost.state
                                   for ghost in self._game.ghosts}
        self._background: pygame.Surface | None = None

        now = perf_counter()
        self.__last_pacman_frame_time = now
        self.__last_frame_time = {ghost.id: now for ghost in self._game.ghosts}

    def __load_assets(self) -> None:
        """
        Load and manage the rendering of game assets, including ghosts and
        their states.

        This method handles the flashing effect of ghosts when they are
        frightened,
        updates their rendering based on their current state (frightened,
        eaten, or normal),
        and manages the animation frames for each ghost. It also ensures
        that the
        rendering is performed at appropriate intervals to create a smooth
        visual experience.

        Args:
            frightened_timer (float): The timer indicating how long the ghosts
            are frightened.

        Returns:
            None
        """
        if self.__assets_loaded:
            return
        self.__pacman_sprites = pygame.image.load(
            PACMAN_SPRITE_PATH)
        self.__ghost_assets: dict[int, pygame.Surface] = {}
        self.__ghost_assets[0] = pygame.image.load(
            BLINKY_SPRITE_PATH)
        self.__ghost_assets[1] = pygame.image.load(
            PINKY_SPRITE_PATH)
        self.__ghost_assets[2] = pygame.image.load(
            INKY_SPRITE_PATH)
        self.__ghost_assets[3] = pygame.image.load(
            CLYDE_SPRITE_PATH)
        self.__pacgum_sprite = pygame.image.load(
            PACGUM_SPRITE_PATH)
        self.__super_pacgum_sprite = pygame.image.load(
            SUPER_PACGUM_SPRITE_PATH)
        self.__dead_ghost_sprite = pygame.image.load(
            "assets/dead_ghost.xpm"
        )
        self.__scared_ghost_sprite = pygame.image.load(
            "assets/scared_ghost.xpm"
        )

    def __update(self, maze: MazeAdapter) -> None:
        """
        Rebuild cached rendering surfaces when the maze or window size changes.

        Checks if the maze instance or the window dimensions differ from the
        cached values, and if so, resizes the window and recreates the
        background, map and wall surfaces used for rendering.

        Args:
            maze (MazeAdapter): The current maze to render.

        Returns:
            None
        """
        if self.maze != maze:
            self.maze = maze
            map_size_x, map_size_y = self.maze.get_size()
            self._map_size_x = map_size_x * CELL_SIZE
            self._map_size_y = map_size_y * CELL_SIZE
            self.__updated = False
        if self._win.get_size() != (self._map_size_x,
                                    self._map_size_y + CELL_SIZE * 2):
            self._win = pygame.display.set_mode(
                (self._map_size_x,
                 self._map_size_y + CELL_SIZE * 2),
                pygame.NOFRAME
                    )
            self._win_size_x, self._win_size_y = self._win.get_size()
            self.__updated = False

        if self.__updated:
            return

        self._map_surface = self._win.subsurface((0, CELL_SIZE,
                                                  self._map_size_x,
                                                  self._map_size_y))
        self._background = pygame.Surface(self._win.get_size())
        self._backgroud_42 = pygame.Surface((CELL_SIZE - WALL_THICKNESS * 2,
                                             CELL_SIZE - WALL_THICKNESS * 2))
        self._ns_wall = pygame.Surface((CELL_SIZE + WALL_THICKNESS * 2,
                                        WALL_THICKNESS))
        self._lw_wall = pygame.Surface((WALL_THICKNESS,
                                        CELL_SIZE + WALL_THICKNESS * 2))

        self._background.fill(BACKGROUND_COLOR)
        self._backgroud_42.fill(FT_BACKGROUND_COLOR)
        self._ns_wall.fill(WALL_COLOR)
        self._lw_wall.fill(WALL_COLOR)

        self.__updated = True

    def _draw_cell(self, cell: Cell, coord: Coordinates) -> None:
        """
        Draw a single maze cell's walls onto the map surface.

        Blits wall segments for each open side (north, east, south, west) of
        the cell at the given coordinates, and draws the 42-logo background
        when the cell is fully enclosed.

        Args:
            cell (Cell): The cell whose walls should be drawn.
            coord (Coordinates): The pixel coordinates of the cell's
            top-left corner.

        Returns:
            None
        """
        x, y = coord
        for i in range(4):
            if cell.n:
                self._map_surface.blit(
                    self._ns_wall,
                    (x - WALL_THICKNESS, y))
            if cell.e:
                self._map_surface.blit(
                    self._lw_wall,
                    (x + (CELL_SIZE - WALL_THICKNESS),
                        y - WALL_THICKNESS))
            if cell.s:
                self._map_surface.blit(
                    self._ns_wall,
                    (x - WALL_THICKNESS,
                        y + (CELL_SIZE - WALL_THICKNESS)))
            if cell.w:
                self._map_surface.blit(
                    self._lw_wall,
                    (x, y - WALL_THICKNESS))
        if cell.e and cell.w and cell.n and cell.s:
            self._map_surface.blit(self._backgroud_42,
                                   (x + WALL_THICKNESS,
                                    y + WALL_THICKNESS))

    def _render_map(self) -> None:
        """
        Render the full maze grid onto the map surface.

        Draws the background, then iterates over every cell in the maze,
        rendering its walls, and adds a final boundary line beneath the
        last row.

        Returns:
            None
        """
        assert self._background
        self._render_surface(self._background, (0, 0))
        final_line = False
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self._draw_cell(
                    self.maze.get_cell(x, y),
                    (x * CELL_SIZE, y * CELL_SIZE)
                    )
                if final_line:
                    self._map_surface.blit(
                        self._ns_wall,
                        (x * CELL_SIZE,
                         self._win_size_y - CELL_SIZE))
            if not final_line:
                final_line = True

    def _render_pacman(self, game_state: GameState, stop: bool) -> None:
        """
        Render Pac-Man's sprite based on the current game state.

        Renders the normal movement animation while the game is playing or
        paused, and switches to the death animation for any other state.

        Args:
            game_state (GameState): The current state of the game.
            stop (bool): A flag indicating whether to stop the animation.

        Returns:
            None
        """
        if game_state in (GameState.PLAYING,
                          GameState.PAUSED):
            self.__pacman_dead_sprite_index_x = 0
            self.__pacman_dead_sprite_index_y = (
                PACMAN_DEATH_SPRITE_START_INDEX_Y)
            self._render_pacman_entity(
                self.__pacman_sprites,
                PACMAN_SPRITE_LAST_INDEX_X,
                stop
                )
            if self.__pacman_last_state != GameState.PLAYING:
                self.__pacman_last_state = GameState.PLAYING
        else:
            self._render_pacman_death(
                self.__pacman_sprites,
                PACMAN_SPRITE_LAST_INDEX_X,
                PACMAN_DEATH_SPRITE_LAST_INDEX_Y,
                PACMAN_DEATH_SPRITE_START_INDEX_Y,
                stop
            )

    def _render_ghosts(self, frightened_timer: float, stop: bool) -> None:
        """
        Render the ghosts in the game.

        This method updates the position of the ghost sprites based on their
        current direction and movement progress. It handles the rendering of
        the sprites on the game surface and manages the animation frames for
        the ghost entities.

        Args:
            frightened_timer (float): The timer indicating how long the ghosts
            are frightened.
            stop (bool): A flag indicating whether to stop rendering.

        Returns:
            None
        """
        now = perf_counter()
        if frightened_timer == 0.0:
            self.__flashing = False
        elif frightened_timer >= TIMER_FRIGHTENED * 0.9:
            if now - self.__last_flash >= TIMER_FRIGHTENED * 0.01:
                self.__flashing = not self.__flashing
                self.__last_flash = now
        elif frightened_timer >= TIMER_FRIGHTENED * 0.75:
            if now - self.__last_flash >= TIMER_FRIGHTENED * 0.03:
                self.__flashing = not self.__flashing
                self.__last_flash = now
        elif frightened_timer >= TIMER_FRIGHTENED * 0.5:
            if now - self.__last_flash >= TIMER_FRIGHTENED * 0.05:
                self.__flashing = not self.__flashing
                self.__last_flash = now
        for i, ghost in enumerate(self._game.ghosts):
            if ghost.state == GhostState.FRIGHTENED:
                self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    ghost,
                    GHOST_SPRITE_LAST_INDEX_X,
                    stop
                    )
            elif ghost.state == GhostState.EATEN:
                self._render_ghost(
                    self.__dead_ghost_sprite,
                    ghost,
                    DEAD_GHOST_SPRITE_LAST_INDEX_X,
                    stop
                    )
                if self.__last_ghost_state[ghost.id] != ghost.state:
                    self.__last_ghost_state[ghost.id] = ghost.state
            else:
                self._render_ghost(
                    self.__ghost_assets[i],
                    ghost,
                    GHOST_SPRITE_LAST_INDEX_X,
                    stop
                    )
                if self.__last_ghost_state[ghost.id] != ghost.state:
                    self.__last_ghost_state[ghost.id] = ghost.state

    def _render_pacgums(self) -> None:
        """
        Render the ghost sprite on the game surface and manage the animation
        frames for the ghost entity.

        This method updates the position of the ghost sprite based on its
        current direction and movement progress. It handles the rendering of
        the sprite on the game surface and manages the animation frames for
        the ghost entity.

        Args:
            sprite (pygame.Surface): The surface on which to render the game
            elements.
            ghost (Ghost): The ghost entity to be rendered.
            last_index_x (int): The last x-coordinate index for rendering.
            stop (bool): A flag indicating whether to stop rendering.

        Returns:
            None
        """
        for pos in self._game.collectables:
            if isinstance(self._game.collectables[pos], Pacgum):
                self._map_surface.blit(
                    self.__pacgum_sprite,
                    (pos[0] * CELL_SIZE + WALL_OFFSET,
                     pos[1] * CELL_SIZE + WALL_OFFSET))
            elif isinstance(self._game.collectables[pos], SuperPacgum):
                self._map_surface.blit(
                    self.__super_pacgum_sprite,
                    (pos[0] * CELL_SIZE + WALL_THICKNESS,
                     pos[1] * CELL_SIZE + WALL_OFFSET))

    def _render_scared_ghost(self, sprite: pygame.Surface,
                             ghost: Ghost,
                             last_index_x: int,
                             stop: bool) -> None:
        """
        Render a scared ghost entity on the game surface.

        This method updates the position of the ghost sprite based on its
        current
        direction and movement progress. It handles the rendering of the
        sprite on
        the game surface and manages the animation frames for the ghost entity.

        Args:
            sprite (pygame.Surface): The surface on which to render the game
            elements.
            ghost (Ghost): The ghost entity to be rendered.
            last_index_x (int): The last x-coordinate index for rendering.
            stop (bool): A flag indicating whether to stop rendering.

        Returns:
            None
        """
        progress_tuple: tuple[float, float]
        match ghost.direction:
            case Direction.NORTH:
                progress_tuple = (0.0, -ghost.move_progress)
            case Direction.EAST:
                progress_tuple = (ghost.move_progress, 0.0)
            case Direction.SOUTH:
                progress_tuple = (0.0, ghost.move_progress)
            case Direction.WEST:
                progress_tuple = (-ghost.move_progress, 0.0)
            case _:
                raise ValueError("Invalid direction")

        if self.__flashing:
            self._map_surface.blit(
                sprite,
                ((ghost.pos[0]
                  + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
                 (ghost.pos[1]
                  + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
                (self.__sprites_x[ghost.id] * SPRITE_SIZE,
                 FLASHING_GHOST_SPRITE_INDEX_Y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                 )

        else:
            self._map_surface.blit(
                sprite,
                ((ghost.pos[0]
                  + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
                 (ghost.pos[1]
                  + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
                (self.__sprites_x[ghost.id] * SPRITE_SIZE,
                 SCARED_GHOST_SPRITE_INDEX_Y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                 )

        if stop:
            return
        now = perf_counter()
        if not (
             now - self.__last_frame_time[ghost.id] >= self._animation_fps):
            return
        self.__last_frame_time[ghost.id] = now
        if self.__sprites_x[ghost.id] == last_index_x:
            self.__sprites_x[ghost.id] = 0
        else:
            self.__sprites_x[ghost.id] += 1

    def _render_ghost(self, sprite: pygame.Surface,
                      ghost: Ghost, last_index_x: int,
                      stop: bool) -> None:
        """
        Render the ghost sprite on the game surface and manage the animation
        frames for the Pac-Man entity.

        Args:
            sprite (pygame.Surface): The surface on which to render the game
            elements.
            ghost (Ghost): The ghost entity to be rendered.
            last_index_x (int): The last x-coordinate index for rendering.
            stop (bool): A flag indicating whether to stop rendering.

        Returns:
            None
        """
        progress_tuple: tuple[float, float]
        match ghost.direction:
            case Direction.NORTH:
                self.__sprites_y[ghost.id] = ENTITIES_UP_SPRITE_INDEX_Y
                progress_tuple = (0.0, -ghost.move_progress)
            case Direction.EAST:
                self.__sprites_y[ghost.id] = ENTITIES_RIGHT_SPRITE_INDEX_Y
                progress_tuple = (ghost.move_progress, 0.0)
            case Direction.WEST:
                self.__sprites_y[ghost.id] = ENTITIES_LEFT_SPRITE_INDEX_Y
                progress_tuple = (-ghost.move_progress, 0.0)
            case Direction.SOUTH:
                self.__sprites_y[ghost.id] = ENTITIES_DOWN_SPRITE_INDEX_Y
                progress_tuple = (0.0, ghost.move_progress)
            case _:
                raise ValueError("Invalid direction")

        if ghost.state == GhostState.EATEN:
            self._map_surface.blit(
                sprite,
                ((ghost.pos[0]
                  + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
                 (ghost.pos[1]
                  + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
                (0 * SPRITE_SIZE,
                 self.__sprites_y[ghost.id] * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                )
            return

        self._map_surface.blit(
            sprite,
            ((ghost.pos[0]
              + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
             (ghost.pos[1]
              + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
            (self.__sprites_x[ghost.id] * SPRITE_SIZE,
             self.__sprites_y[ghost.id] * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
            )

        if stop:
            return
        now = perf_counter()
        if not (now - self.__last_frame_time[ghost.id] >= self._animation_fps):
            return
        self.__last_frame_time[ghost.id] = now
        if self.__sprites_x[ghost.id] == last_index_x:
            self.__sprites_x[ghost.id] = 0
        else:
            self.__sprites_x[ghost.id] += 1

    def _render_pacman_entity(self, sprite: pygame.Surface,
                              last_index_x: int,
                              stop: bool) -> None:
        """
        Render the Pac-Man entity on the game surface.

        This method updates the position of the Pac-Man sprite
        based on its current
        direction and movement progress. It handles the rendering
        of the sprite on
        the game surface and manages the animation frames for the
        Pac-Man entity.

        Args:
            sprite (pygame.Surface): The surface on which to render the
            game elements.
            last_index_x (int): The last x-coordinate index for rendering.
            last_index_y (int): The last y-coordinate index for rendering.
            start_index_y (int): The starting y-coordinate index for rendering.
            stop (bool): A flag indicating whether to stop rendering.

        Returns:
            None
        """
        progress_tuple: tuple[float, float]
        match self._game.pacman.direction:
            case Direction.NORTH:
                if self._game.pacman.reversing:
                    progress_tuple = (0.0, self._game.pacman.move_progress)
                else:
                    progress_tuple = (0.0, -self._game.pacman.move_progress)
                self.__pacman_sprite_index_y = ENTITIES_UP_SPRITE_INDEX_Y
            case Direction.EAST:
                if self._game.pacman.reversing:
                    progress_tuple = (-self._game.pacman.move_progress, 0.0)
                else:
                    progress_tuple = (self._game.pacman.move_progress, 0.0)
                self.__pacman_sprite_index_y = ENTITIES_RIGHT_SPRITE_INDEX_Y
            case Direction.WEST:
                if self._game.pacman.reversing:
                    progress_tuple = (self._game.pacman.move_progress, 0.0)
                else:
                    progress_tuple = (-self._game.pacman.move_progress, 0.0)
                self.__pacman_sprite_index_y = ENTITIES_LEFT_SPRITE_INDEX_Y
            case Direction.SOUTH:
                if self._game.pacman.reversing:
                    progress_tuple = (0.0, -self._game.pacman.move_progress)
                else:
                    progress_tuple = (0.0, self._game.pacman.move_progress)
                self.__pacman_sprite_index_y = ENTITIES_DOWN_SPRITE_INDEX_Y
            case _:
                raise ValueError("Invalid direction")

        self._map_surface.blit(
            sprite,
            ((self._game.pacman.pos[0] + progress_tuple[0])
                * CELL_SIZE + WALL_OFFSET,
             (self._game.pacman.pos[1] + progress_tuple[1])
                * CELL_SIZE + WALL_OFFSET),
            (self.__pacman_sprite_index_x * SPRITE_SIZE,
             self.__pacman_sprite_index_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
            )

        if stop:
            return
        now = perf_counter()
        if not (now - self.__last_pacman_frame_time >= self._animation_fps):
            return
        self.__last_pacman_frame_time = now
        if self.__pacman_sprite_index_x == last_index_x:
            self.__pacman_sprite_index_x = 0
        else:
            self.__pacman_sprite_index_x += 1

    def _render_pacman_death(self, sprite: pygame.Surface,
                             last_index_x: int,
                             last_index_y: int,
                             start_index_y: int,
                             stop: bool) -> None:
        """
        Renders the current state of the game, including the maze,
        Pac-Man, and ghosts.
        Handles the logic for ghost states and pauses the game if necessary.

        Args:
            sprite (pygame.Surface): The surface on which to render the game
            elements.
            last_index_x (int): The last x-coordinate index for rendering.
            last_index_y (int): The last y-coordinate index for rendering.
            start_index_y (int): The starting y-coordinate index for rendering.
            stop (bool): A flag indicating whether to stop rendering.

        Returns:
            None
        """
        progress_tuple: tuple[float, float]
        match self._game.pacman.direction:
            case Direction.NORTH:
                if self._game.pacman.reversing:
                    progress_tuple = (0.0, self._game.pacman.move_progress)
                else:
                    progress_tuple = (0.0, -self._game.pacman.move_progress)
            case Direction.EAST:
                if self._game.pacman.reversing:
                    progress_tuple = (-self._game.pacman.move_progress, 0.0)
                else:
                    progress_tuple = (self._game.pacman.move_progress, 0.0)
            case Direction.WEST:
                if self._game.pacman.reversing:
                    progress_tuple = (self._game.pacman.move_progress, 0.0)
                else:
                    progress_tuple = (-self._game.pacman.move_progress, 0.0)
            case Direction.SOUTH:
                if self._game.pacman.reversing:
                    progress_tuple = (0.0, -self._game.pacman.move_progress)
                else:
                    progress_tuple = (0.0, self._game.pacman.move_progress)
            case _:
                raise ValueError("Invalid direction")
        self._map_surface.blit(
            sprite,
            ((self._game.pacman.pos[0] + progress_tuple[0])
                * CELL_SIZE + WALL_OFFSET,
             (self._game.pacman.pos[1] + progress_tuple[1])
                * CELL_SIZE + WALL_OFFSET),
            (self.__pacman_dead_sprite_index_x * SPRITE_SIZE,
             self.__pacman_dead_sprite_index_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
             )

        if stop:
            return
        now = perf_counter()
        if not (now - self.__last_pacman_frame_time >= self._animation_fps):
            return
        self.__last_pacman_frame_time = now
        if self.__pacman_dead_sprite_index_x == last_index_x:
            self.__pacman_dead_sprite_index_x = 0
            if self.__pacman_dead_sprite_index_y == last_index_y:
                self.__pacman_dead_sprite_index_y = start_index_y
            else:
                self.__pacman_dead_sprite_index_y += 1
        else:
            self.__pacman_dead_sprite_index_x += 1

    def render_gameplay(self, frightened_timer: float,
                        game_state: GameState, maze: MazeAdapter,
                        stop: bool = False) -> None:
        """
        Render the gameplay elements including the map, Pac-Man, and ghosts.

        This method updates the game state, loads necessary assets,
        and renders the
        current state of the game, including the maze, Pac-Man, and ghosts.
        It also
        handles the logic for ghost states and pauses the game if necessary.

        Args:
            frightened_timer (float): The timer indicating how long the ghosts
            are
                frightened.
            game_state (GameState): The current state of the game, which can
            affect
                rendering behavior.
            maze (MazeAdapter): The maze structure that defines the layout of
            the game.
            stop (bool, optional): A flag indicating whether to stop rendering.
                Defaults to False.

        Returns:
            None
        """
        self.__update(maze)
        self.__load_assets()
        self._render_map()
        self._render_pacgums()
        if not self.__wait:
            for ghost in self._game.ghosts:
                if (self.__last_ghost_state[ghost.id] != ghost.state
                        and ghost.state == GhostState.EATEN):
                    stop = True
                    self.__wait = True
            if (self._game.game_state == GameState.RESPAWNING
                    and self.__pacman_last_state != GameState.RESPAWNING):
                stop = True
                self.__wait = True
                self.__pacman_last_state = self._game.game_state
        if self.__wait:
            if self.__wait_timer == 0.0:
                self.__wait_timer = perf_counter()
            if perf_counter() - self.__wait_timer >= DEATH_FREEZE_DURATION:
                self.__wait = False
                self.__wait_timer = 0.0
                self._game.toggle_pause()
            else:
                if game_state != GameState.PAUSED:
                    self._game.toggle_pause()
                stop = True

        self._render_pacman(game_state, stop)
        if not game_state == GameState.RESPAWNING or self.__wait:
            self._render_ghosts(frightened_timer, stop)
