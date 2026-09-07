import pygame
from time import perf_counter
from game import GameState, Entities
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
        close_cell = True
        for direction in cell:
            if cell[direction]:
                match direction:
                    case "N":
                        self._map_surface.blit(
                            self._ns_wall,
                            (x - WALL_THICKNESS, y))
                    case "L":
                        self._map_surface.blit(
                            self._lw_wall,
                            (x + (CELL_SIZE - WALL_THICKNESS),
                             y - WALL_THICKNESS))
                    case "S":
                        self._map_surface.blit(
                            self._ns_wall,
                            (x - WALL_THICKNESS,
                             y + (CELL_SIZE - WALL_THICKNESS)))
                    case "W":
                        self._map_surface.blit(
                            self._lw_wall,
                            (x, y - WALL_THICKNESS))
                    case _:
                        pass
            else:
                close_cell = False
        if close_cell:
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
        if self._game_state.player.alive:
            self._game_state.player.dead_sprite_x = 0
            self._game_state.player.dead_sprite_y = (
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

        if self._game_state.clyde.scared:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.clyde,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.clyde.alive:
            self._render_entitie(self.__clyde_sprites,
                                 self._game_state.clyde,
                                 GHOST_SPRITE_LAST_INDEX_X)

        else:
            self._render_entitie(self.__dead_ghost_sprite,
                                 self._game_state.clyde,
                                 DEAD_GHOST_SPRITE_LAST_INDEX_X)

        if self._game_state.inky.scared:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.inky,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.inky.alive:
            self._render_entitie(self.__inky_sprites,
                                 self._game_state.inky,
                                 GHOST_SPRITE_LAST_INDEX_X)

        else:
            self._render_entitie(self.__dead_ghost_sprite,
                                 self._game_state.inky,
                                 DEAD_GHOST_SPRITE_LAST_INDEX_X)

        if self._game_state.blinky.scared:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.blinky,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.blinky.alive:
            self._render_entitie(self.__blinky_sprites,
                                 self._game_state.blinky,
                                 GHOST_SPRITE_LAST_INDEX_X)

        else:
            self._render_entitie(self.__dead_ghost_sprite,
                                 self._game_state.blinky,
                                 DEAD_GHOST_SPRITE_LAST_INDEX_X)

        if self._game_state.pinky.scared:
            self._render_scared_ghost(
                    self.__scared_ghost_sprite,
                    self._game_state.pinky,
                    GHOST_SPRITE_LAST_INDEX_X
                )

        elif self._game_state.pinky.alive:
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
                             entitie: Entities, last_index_x: int) -> None:
        if self._game_state.flashing:
            self._map_surface.blit(
                sprite,
                (entitie.pos[0] * CELL_SIZE + WALL_OFFSET,
                 entitie.pos[1] * CELL_SIZE + WALL_OFFSET),
                (entitie.sprite_x * SPRITE_SIZE,
                 FLASHING_GHOST_SPRITE_INDEX_Y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                 )

        else:
            self._map_surface.blit(
                sprite,
                (entitie.pos[0] * CELL_SIZE + WALL_OFFSET,
                 entitie.pos[1] * CELL_SIZE + WALL_OFFSET),
                (entitie.sprite_x * SPRITE_SIZE,
                 SCARED_GHOST_SPRITE_INDEX_Y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                 )

        now = perf_counter()
        if not (now - entitie.last_frame_time >= self._animation_fps):
            return
        entitie.last_frame_time = now
        if entitie.sprite_x == last_index_x:
            entitie.sprite_x = 0
        else:
            entitie.sprite_x += 1

    def _render_entitie(self, sprite: pygame.Surface,
                        entitie: Entities, last_index_x: int) -> None:
        match entitie.direction:
            case 'N':
                entitie.sprite_y = ENTITIES_UP_SPRITE_INDEX_Y
            case 'L':
                entitie.sprite_y = ENTITIES_RIGHT_SPRITE_INDEX_Y
            case 'W':
                entitie.sprite_y = ENTITIES_LEFT_SPRITE_INDEX_Y
            case 'S':
                entitie.sprite_y = ENTITIES_DOWN_SPRITE_INDEX_Y

        if not entitie.alive:
            self._map_surface.blit(
                sprite,
                (entitie.pos[0] * CELL_SIZE + WALL_OFFSET,
                 entitie.pos[1] * CELL_SIZE + WALL_OFFSET),
                (0 * SPRITE_SIZE,
                 entitie.sprite_y * SPRITE_SIZE,
                 SPRITE_SIZE, SPRITE_SIZE)
                )
            return

        self._map_surface.blit(
            sprite,
            (entitie.pos[0] * CELL_SIZE + WALL_OFFSET,
             entitie.pos[1] * CELL_SIZE + WALL_OFFSET),
            (entitie.sprite_x * SPRITE_SIZE,
             entitie.sprite_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
            )

        now = perf_counter()
        if not (now - entitie.last_frame_time >= self._animation_fps):
            return
        entitie.last_frame_time = now
        if entitie.sprite_x == last_index_x:
            entitie.sprite_x = 0
        else:
            entitie.sprite_x += 1

    def _render_entitie_death(self, sprite: pygame.Surface,
                              entitie: Entities,
                              last_index_x: int,
                              last_index_y: int,
                              start_index_y: int) -> None:
        self._map_surface.blit(
            sprite,
            (entitie.pos[0] * CELL_SIZE + WALL_OFFSET,
             entitie.pos[1] * CELL_SIZE + WALL_OFFSET),
            (entitie.dead_sprite_x * SPRITE_SIZE,
             entitie.dead_sprite_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)
             )

        now = perf_counter()
        if not (now - entitie.last_frame_time >= self._animation_fps):
            return
        entitie.last_frame_time = now
        if entitie.dead_sprite_x == last_index_x:
            entitie.dead_sprite_x = 0
            if entitie.dead_sprite_y == last_index_y:
                entitie.dead_sprite_y = start_index_y
            else:
                entitie.dead_sprite_y += 1
        else:
            entitie.dead_sprite_x += 1

    def render_gameplay(self) -> None:
        self.__update()
        self.__load_assets()
        self._render_map()
        self._render_pacgums()
        self._render_pacman()
        if self._game_state.player.alive:
            self._render_ghosts()
