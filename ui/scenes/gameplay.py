import pygame
from time import perf_counter
from enums import Direction, GhostState
from entities import MovableEntity
from game import GameState
from maze import Cell
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
    DEAD_GHOST_SPRITE_LAST_INDEX_X, SCARED_TIME, FLASHING_GHOST_SPRITE_INDEX_Y,
    SCARED_GHOST_SPRITE_INDEX_Y
    )


Coordinates = tuple[int, int]


class Gameplay(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game_state: GameState, map_size: tuple[int, int]) -> None:
        super().__init__(win_size, title, game_state)
        map_size_x, map_size_y = map_size
        self._map_size_x = map_size_x * CELL_SIZE
        self._map_size_y = map_size_y * CELL_SIZE
        self.__assets_loaded = False
        self.__updated = False
        self.__last_flash = 0.0
        self.__alive_sprites_y = {
            self._game_state.player: 0,
            self._game_state.blinky: 0,
            self._game_state.inky: 0,
            self._game_state.pinky: 0,
            self._game_state.clyde: 0}
        self.__alive_sprites_x = {
            self._game_state.player: 0,
            self._game_state.blinky: 0,
            self._game_state.inky: 0,
            self._game_state.pinky: 0,
            self._game_state.clyde: 0}

        self.__dead_sprites_y = {
            self._game_state.player: PACMAN_DEATH_SPRITE_START_INDEX_Y,
            self._game_state.blinky: 0,
            self._game_state.inky: 0,
            self._game_state.pinky: 0,
            self._game_state.clyde: 0}
        self.__dead_sprites_x = {
            self._game_state.player: 0,
            self._game_state.blinky: 0,
            self._game_state.inky: 0,
            self._game_state.pinky: 0,
            self._game_state.clyde: 0}
        now = perf_counter()
        self.__last_frame_time = {
            self._game_state.player: now,
            self._game_state.blinky: now,
            self._game_state.inky: now,
            self._game_state.pinky: now,
            self._game_state.clyde: now}

    def __load_assets(self) -> None:
        if self.__assets_loaded:
            return
        self.__pacman_sprites = pygame.image.load(
            PACMAN_SPRITE_PATH)
        self.__blinky_sprites = pygame.image.load(
            BLINKY_SPRITE_PATH)
        self.__inky_sprites = pygame.image.load(
            INKY_SPRITE_PATH)
        self.__pinky_sprites = pygame.image.load(
            PINKY_SPRITE_PATH)
        self.__clyde_sprites = pygame.image.load(
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
        for y in range(self._game_state.maze.height):
            for x in range(self._game_state.maze.width):
                self._draw_cell(
                    self._game_state.maze.get_cell(x, y),
                    (x * CELL_SIZE, y * CELL_SIZE))
                if final_line:
                    self._map_surface.blit(
                        self._ns_wall,
                        (x * CELL_SIZE,
                         self._win_size_y - CELL_SIZE))
            if not final_line:
                final_line = True

    def _render_pacman(self) -> None:
        if self._game_state.alive:
            self.__dead_sprites_x[self._game_state.player] = 0
            self.__dead_sprites_y[self._game_state.player] = (
                PACMAN_DEATH_SPRITE_START_INDEX_Y
                )
            self._render_entitie(self.__pacman_sprites,
                                 self._game_state.player,
                                 PACMAN_SPRITE_LAST_INDEX_X)
        else:
            self._render_entitie_death(
                self.__pacman_sprites,
                self._game_state.player,
                PACMAN_SPRITE_LAST_INDEX_X,
                PACMAN_DEATH_SPRITE_LAST_INDEX_Y,
                PACMAN_DEATH_SPRITE_START_INDEX_Y
            )

    def _render_ghosts(self) -> None:
        now = perf_counter()
        if now - self._game_state.scared_start_time >= SCARED_TIME * 3 / 4:
            if now - self.__last_flash >= SCARED_TIME * 0.02:
                self._game_state.flashing = not self._game_state.flashing
                self.__last_flash = now
        elif now - self._game_state.scared_start_time >= SCARED_TIME * 2 / 4:
            if now - self.__last_flash >= SCARED_TIME * 0.05:
                self._game_state.flashing = not self._game_state.flashing
                self.__last_flash = now

        if self._game_state.clyde.state == GhostState.FRIGHTENED:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.clyde,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.clyde.state == GhostState.CHASE:
            self._render_entitie(self.__clyde_sprites,
                                 self._game_state.clyde,
                                 GHOST_SPRITE_LAST_INDEX_X)

        else:
            self._render_entitie(self.__dead_ghost_sprite,
                                 self._game_state.clyde,
                                 DEAD_GHOST_SPRITE_LAST_INDEX_X)

        if self._game_state.inky.state == GhostState.FRIGHTENED:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.inky,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.inky.state == GhostState.CHASE:
            self._render_entitie(self.__inky_sprites,
                                 self._game_state.inky,
                                 GHOST_SPRITE_LAST_INDEX_X)

        else:
            self._render_entitie(self.__dead_ghost_sprite,
                                 self._game_state.inky,
                                 DEAD_GHOST_SPRITE_LAST_INDEX_X)

        if self._game_state.blinky.state == GhostState.FRIGHTENED:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.blinky,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.blinky.state == GhostState.CHASE:
            self._render_entitie(self.__blinky_sprites,
                                 self._game_state.blinky,
                                 GHOST_SPRITE_LAST_INDEX_X)

        else:
            self._render_entitie(self.__dead_ghost_sprite,
                                 self._game_state.blinky,
                                 DEAD_GHOST_SPRITE_LAST_INDEX_X)

        if self._game_state.pinky.state == GhostState.FRIGHTENED:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.pinky,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.pinky.state == GhostState.CHASE:
            self._render_entitie(self.__pinky_sprites,
                                 self._game_state.pinky,
                                 GHOST_SPRITE_LAST_INDEX_X)
        else:
            self._render_entitie(self.__dead_ghost_sprite,
                                 self._game_state.pinky,
                                 DEAD_GHOST_SPRITE_LAST_INDEX_X)

    def _render_pacgums(self) -> None:
        self._map_surface.blit(self.__pacgum_sprite,
                               (1 * CELL_SIZE + WALL_OFFSET,
                                5 * CELL_SIZE + WALL_OFFSET))
        self._map_surface.blit(self.__super_pacgum_sprite,
                               (1 * CELL_SIZE + WALL_THICKNESS,
                                6 * CELL_SIZE + WALL_OFFSET))

    def _render_scared_ghost(self, sprite: pygame.Surface,
                             entity: MovableEntity,
                             last_index_x: int) -> None:
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

        if self._game_state.flashing:
            self._map_surface.blit(
                sprite,
                ((entity.pos[0]
                  + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
                 (entity.pos[1]
                  + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
                (self.__alive_sprites_x[entity] * SPRITE_SIZE,
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
                (self.__alive_sprites_x[entity] * SPRITE_SIZE,
                 SCARED_GHOST_SPRITE_INDEX_Y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                 )

        now = perf_counter()
        if not (now - self.__last_frame_time[entity] >= self._animation_fps):
            return
        self.__last_frame_time[entity] = now
        if self.__alive_sprites_x[entity] == last_index_x:
            self.__alive_sprites_x[entity] = 0
        else:
            self.__alive_sprites_x[entity] += 1

    def _render_entitie(self, sprite: pygame.Surface,
                        entity: MovableEntity, last_index_x: int) -> None:
        progress_tuple: tuple[float, float]
        match entity.direction:
            case Direction.NORTH:
                self.__alive_sprites_y[entity] = ENTITIES_UP_SPRITE_INDEX_Y
                progress_tuple = (0.0, -entity.move_progress)
            case Direction.EAST:
                self.__alive_sprites_y[entity] = ENTITIES_RIGHT_SPRITE_INDEX_Y
                progress_tuple = (entity.move_progress, 0.0)
            case Direction.WEST:
                self.__alive_sprites_y[entity] = ENTITIES_LEFT_SPRITE_INDEX_Y
                progress_tuple = (-entity.move_progress, 0.0)
            case Direction.SOUTH:
                self.__alive_sprites_y[entity] = ENTITIES_DOWN_SPRITE_INDEX_Y
                progress_tuple = (0.0, entity.move_progress)
            case _:
                raise ValueError("Invalid direction")

        if not self._game_state.alive: # trocar para entity
            self._map_surface.blit(
                sprite,
                ((entity.pos[0]
                  + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
                 (entity.pos[1]
                  + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
                (0 * SPRITE_SIZE,
                 self.__alive_sprites_y[entity] * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                )
            return

        self._map_surface.blit(
            sprite,
            ((entity.pos[0]
              + progress_tuple[0]) * CELL_SIZE + WALL_OFFSET,
             (entity.pos[1]
              + progress_tuple[1]) * CELL_SIZE + WALL_OFFSET),
            (self.__alive_sprites_x[entity] * SPRITE_SIZE,
             self.__alive_sprites_y[entity] * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
            )

        now = perf_counter()
        if not (now - self.__last_frame_time[entity] >= self._animation_fps):
            return
        self.__last_frame_time[entity] = now
        if self.__alive_sprites_x[entity] == last_index_x:
            self.__alive_sprites_x[entity] = 0
        else:
            self.__alive_sprites_x[entity] += 1

    def _render_entitie_death(self, sprite: pygame.Surface,
                              entity: MovableEntity,
                              last_index_x: int,
                              last_index_y: int,
                              start_index_y: int) -> None:
        self._map_surface.blit(
            sprite,
            (entity.pos[0] * CELL_SIZE + WALL_OFFSET,
             entity.pos[1] * CELL_SIZE + WALL_OFFSET),
            (self.__dead_sprites_x[entity] * SPRITE_SIZE,
             self.__dead_sprites_y[entity] * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
             )

        now = perf_counter()
        if not (now - self.__last_frame_time[entity] >= self._animation_fps):
            return
        self.__last_frame_time[entity] = now
        if self.__dead_sprites_x[entity] == last_index_x:
            self.__dead_sprites_x[entity] = 0
            if self.__dead_sprites_y[entity] == last_index_y:
                self.__dead_sprites_y[entity] = start_index_y
            else:
                self.__dead_sprites_y[entity] += 1
        else:
            self.__dead_sprites_x[entity] += 1

    def render_gameplay(self) -> None:
        self.__update()
        self.__load_assets()
        self._render_map()
        self._render_pacgums()
        self._render_pacman()
        if self._game_state.alive:
            self._render_ghosts()
