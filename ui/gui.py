import pygame
from .scenes import MainMenu, Instructions, Gameplay
from game import GameState
from maze import Cell
from consts import (WALL_THICKNESS, CELL_SIZE, BACKGROUND_COLOR,
                    FT_BACKGROUND_COLOR, WALL_COLOR)


Coordinates = tuple[int, int]


class GUI:
    def __init__(self, title: str, size: tuple[int, int]) -> None:
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
        self.main_menu = MainMenu(self.screen)
        self.instructions_menu = Instructions(self.screen)
        self.gameplay = Gameplay(self.screen)

        self.ns_wall = pygame.Surface((CELL_SIZE + WALL_THICKNESS * 2,
                                       WALL_THICKNESS))
        self._fill(self.ns_wall, WALL_COLOR)

        self.lw_wall = pygame.Surface((WALL_THICKNESS,
                                       CELL_SIZE + WALL_THICKNESS * 2))
        self._fill(self.lw_wall, WALL_COLOR)

        self.background = pygame.Surface(self.screen.get_size())
        self._fill(self.background, BACKGROUND_COLOR)

        self.backgroud_42 = pygame.Surface((CELL_SIZE - WALL_THICKNESS * 2,
                                            CELL_SIZE - WALL_THICKNESS * 2))
        self._fill(self.backgroud_42, FT_BACKGROUND_COLOR)

    def draw(self, game_state: GameState):
        draw_func = getattr(self, game_state.active_screen)
        assert draw_func is not None
        draw_func(game_state)
        self.screen.blit(pygame.font.SysFont(None, 30).render(
            f"{round(game_state.clock.get_fps())}", 1, (255, 255, 255)),
                         (80, 80))  # debug
        pygame.display.update()

    def menu(self, game_state: GameState):
        self._fill(self.screen, BACKGROUND_COLOR)
        self.main_menu.render_menu(game_state=game_state)

    def game(self, game_state: GameState):
        self.screen.blit(self.background, (0, 0))
        for y in range(game_state.maze.height):
            for x in range(game_state.maze.width):
                self._draw_cell(game_state.maze.get_cell(x, y),
                                (x * CELL_SIZE, y * CELL_SIZE))
        self.gameplay.debug_animate()
        self.gameplay.draw_entities(game_state)

    def instructions(self, *args):
        self._fill(self.screen, BACKGROUND_COLOR)
        self.instructions_menu.render_instructions()

    def get_event(self) -> list[pygame.event.Event]:
        events = pygame.event.get()
        return events

    def _draw_cell(self, cell: Cell, coord: Coordinates) -> None:
        x, y = coord
        close_cell = True
        for direction in cell:
            if cell[direction]:
                match direction:
                    case "N":
                        self.screen.blit(self.ns_wall,
                                         (x - WALL_THICKNESS, y))
                    case "L":
                        self.screen.blit(self.lw_wall,
                                         (x + (CELL_SIZE - WALL_THICKNESS),
                                          y - WALL_THICKNESS))
                    case "S":
                        self.screen.blit(self.ns_wall,
                                         (x - WALL_THICKNESS,
                                          y + (CELL_SIZE - WALL_THICKNESS)
                                          ))
                    case "W":
                        self.screen.blit(self.lw_wall,
                                         (x, y - WALL_THICKNESS))
                    case _:
                        pass
            else:
                close_cell = False
        if close_cell:
            self.screen.blit(self.backgroud_42,
                             (x + WALL_THICKNESS,
                              y + WALL_THICKNESS))

    def _fill(self, surface: pygame.Surface,
              color: tuple[int, int, int]) -> None:
        pygame.PixelArray(surface)[:] = color  # type: ignore

    def quit(self) -> None:
        pygame.quit()
