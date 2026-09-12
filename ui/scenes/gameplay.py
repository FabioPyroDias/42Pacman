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
    )


Coordinates = tuple[int, int]


class Gameplay(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter,
                 map_size: tuple[int, int], *args) -> None:
        super().__init__(win_size, title, game, maze, *args)
        map_size_x, map_size_y = map_size
        self._map_size_x = map_size_x * CELL_SIZE
        self._map_size_y = map_size_y * CELL_SIZE
        self.__assets_loaded = False
        self.__updated = False
        self.__flashing = False
        self.__last_flash = 0.0
        self.__pacman_sprite_index_x = 0
        self.__pacman_sprite_index_y = 0
        self.__pacman_dead_sprite_index_x = 0
        self.__pacman_dead_sprite_index_y = PACMAN_DEATH_SPRITE_START_INDEX_Y
        self.__sprites_y = {ghost.id: 0 for ghost in self._game.ghosts}
        self.__sprites_x = {ghost.id: 0 for ghost in self._game.ghosts}

        now = perf_counter()
        self.__last_pacman_frame_time = now
        self.__last_frame_time = {ghost.id: now for ghost in self._game.ghosts}

    def __load_assets(self) -> None:
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

    def __update(self) -> None:
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

        self._fill(self._background, BACKGROUND_COLOR)
        self._fill(self._backgroud_42, FT_BACKGROUND_COLOR)
        self._fill(self._ns_wall, WALL_COLOR)
        self._fill(self._lw_wall, WALL_COLOR)

        self.__updated = True

    def _draw_cell(self, cell: Cell, coord: Coordinates) -> None:
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
        self._render_surface(self._background, (0, 0))
        final_line = False
        for y in range(self._maze.height):
            for x in range(self._maze.width):
                self._draw_cell(
                    self._maze.get_cell(x, y),
                    (x * CELL_SIZE, y * CELL_SIZE)
                    )
                if final_line:
                    self._map_surface.blit(
                        self._ns_wall,
                        (x * CELL_SIZE,
                         self._win_size_y - CELL_SIZE))
            if not final_line:
                final_line = True

    def _render_pacman(self, game_state: GameState) -> None:
        if game_state in (GameState.PLAYING,
                          GameState.PAUSED):
            self.__pacman_dead_sprite_index_x = 0
            self.__pacman_dead_sprite_index_y = (
                PACMAN_DEATH_SPRITE_START_INDEX_Y)
            self._render_pacman_entity(
                self.__pacman_sprites,
                PACMAN_SPRITE_LAST_INDEX_X
                )
        else:
            self._render_entitie_death(
                self.__pacman_sprites,
                PACMAN_SPRITE_LAST_INDEX_X,
                PACMAN_DEATH_SPRITE_LAST_INDEX_Y,
                PACMAN_DEATH_SPRITE_START_INDEX_Y
            )

    def _render_ghosts(self, frightened_timer: float) -> None:
        now = perf_counter()
        if frightened_timer >= TIMER_FRIGHTENED * 0.9:
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
                    GHOST_SPRITE_LAST_INDEX_X
                    )
            elif ghost.state == GhostState.EATEN:
                self._render_ghost(
                    self.__dead_ghost_sprite,
                    ghost,
                    DEAD_GHOST_SPRITE_LAST_INDEX_X
                    )
                self._render_ghost(
                    self.__ghost_assets[i],
                    ghost,
                    GHOST_SPRITE_LAST_INDEX_X
                    )
            else:
                self._render_ghost(
                    self.__ghost_assets[i],
                    ghost,
                    GHOST_SPRITE_LAST_INDEX_X
                    )

    def _render_pacgums(self) -> None:
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
                             entity: Ghost,
                             last_index_x: int,) -> None:
        progress_tuple: tuple[float, float]
        match entity.direction:
            case Direction.NORTH:
                progress_tuple = (0.0, -entity.move_progress)
            case Direction.EAST:
                progress_tuple = (entity.move_progress, 0.0)
            case Direction.SOUTH:
                progress_tuple = (0.0, entity.move_progress)
            case Direction.WEST:
                progress_tuple = (-entity.move_progress, 0.0)
            case _:
                raise ValueError("Invalid direction")

        if self.__flashing:
            self._map_surface.blit(
                sprite,
                ((entity.pos[0]
                  + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
                 (entity.pos[1]
                  + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
                (self.__sprites_x[entity.id] * SPRITE_SIZE,
                 FLASHING_GHOST_SPRITE_INDEX_Y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                 )

        else:
            self._map_surface.blit(
                sprite,
                ((entity.pos[0]
                  + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
                 (entity.pos[1]
                  + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
                (self.__sprites_x[entity.id] * SPRITE_SIZE,
                 SCARED_GHOST_SPRITE_INDEX_Y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                 )

        now = perf_counter()
        if not (
             now - self.__last_frame_time[entity.id] >= self._animation_fps):
            return
        self.__last_frame_time[entity.id] = now
        if self.__sprites_x[entity.id] == last_index_x:
            self.__sprites_x[entity.id] = 0
        else:
            self.__sprites_x[entity.id] += 1

    def _render_ghost(self, sprite: pygame.Surface,
                      ghost: Ghost, last_index_x: int) -> None:
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

        now = perf_counter()
        if not (now - self.__last_frame_time[ghost.id] >= self._animation_fps):
            return
        self.__last_frame_time[ghost.id] = now
        if self.__sprites_x[ghost.id] == last_index_x:
            self.__sprites_x[ghost.id] = 0
        else:
            self.__sprites_x[ghost.id] += 1

    def _render_pacman_entity(self, sprite: pygame.Surface,
                              last_index_x: int) -> None:
        progress_tuple: tuple[float, float]
        match self._game.pacman.direction:
            case Direction.NORTH:
                self.__pacman_sprite_index_y = ENTITIES_UP_SPRITE_INDEX_Y
                progress_tuple = (0.0, -self._game.pacman.move_progress)
            case Direction.EAST:
                self.__pacman_sprite_index_y = ENTITIES_RIGHT_SPRITE_INDEX_Y
                progress_tuple = (self._game.pacman.move_progress, 0.0)
            case Direction.WEST:
                self.__pacman_sprite_index_y = ENTITIES_LEFT_SPRITE_INDEX_Y
                progress_tuple = (-self._game.pacman.move_progress, 0.0)
            case Direction.SOUTH:
                self.__pacman_sprite_index_y = ENTITIES_DOWN_SPRITE_INDEX_Y
                progress_tuple = (0.0, self._game.pacman.move_progress)
            case _:
                raise ValueError("Invalid direction")

        self._map_surface.blit(
            sprite,
            ((self._game.pacman.pos[0]
              + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
             (self._game.pacman.pos[1]
              + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
            (self.__pacman_sprite_index_x * SPRITE_SIZE,
             self.__pacman_sprite_index_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
            )

        now = perf_counter()
        if not (now - self.__last_pacman_frame_time >= self._animation_fps):
            return
        self.__last_pacman_frame_time = now
        if self.__pacman_sprite_index_x == last_index_x:
            self.__pacman_sprite_index_x = 0
        else:
            self.__pacman_sprite_index_x += 1

    def _render_entitie_death(self, sprite: pygame.Surface,
                              last_index_x: int,
                              last_index_y: int,
                              start_index_y: int) -> None:
        self._map_surface.blit(
            sprite,
            (self._game.pacman.pos[0] * CELL_SIZE + WALL_OFFSET,
             self._game.pacman.pos[1] * CELL_SIZE + WALL_OFFSET),
            (self.__pacman_dead_sprite_index_x * SPRITE_SIZE,
             self.__pacman_dead_sprite_index_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
             )

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
                        game_state: GameState) -> None:
        self.__update()
        self.__load_assets()
        self._render_map()
        self._render_pacgums()
        self._render_pacman(game_state)
        if not game_state == GameState.RESPAWNING:
            self._render_ghosts(frightened_timer)
