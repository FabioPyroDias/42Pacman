import pygame
from .scenes import MainMenu
from game import GameState
from maze import MazeAdapter, Cell

Coordinates = tuple[int, int]


WALL_THICKNESS = 5
CELL_SIZE = 50


class GUI:
    def __init__(self, title: str, size: tuple[int, int]) -> None:
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(size)
        self.main_menu = MainMenu(self.screen)
        self.ns_wall = pygame.Surface((CELL_SIZE, WALL_THICKNESS))
        self._fill(self.ns_wall, (255, 255, 255))
        self.lw_wall = pygame.Surface((WALL_THICKNESS, CELL_SIZE))
        self._fill(self.lw_wall, (255, 255, 255))

    def draw(self, game_state: GameState):
        draw_func = getattr(self, game_state.active_screen)
        assert draw_func is not None
        draw_func(maze=game_state.maze)
        pygame.display.update()

    def menu(self, **kwargs):
        self.main_menu.render_menu()

    def game(self, maze: MazeAdapter):
        background = pygame.Surface(self.screen.get_size())
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        for y in range(maze.height):
            for x in range(maze.width):
                self._draw_cell(maze.get_cell(x, y),
                                (x * CELL_SIZE, y * CELL_SIZE))

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()

    def _draw_cell(self, cell: Cell, coord: Coordinates) -> None:
        x, y = coord
        close_cell = True
        for direction in cell:
            if cell[direction]:
                match direction:
                    case "N":
                        self.screen.blit(self.ns_wall,
                                         (x, y))
                    case "L":
                        self.screen.blit(self.lw_wall,
                                         (x + CELL_SIZE, y + WALL_THICKNESS))
                    case "S":
                        self.screen.blit(self.ns_wall,
                                         (x + WALL_THICKNESS, y + CELL_SIZE))
                    case "W":
                        self.screen.blit(self.lw_wall,
                                         (x, y))
                    case _:
                        pass
            else:
                close_cell = False
        if close_cell:
            backgroud_42 = pygame.Surface((CELL_SIZE - WALL_THICKNESS,
                                           CELL_SIZE - WALL_THICKNESS))
            self._fill(backgroud_42, (100, 0, 100))
            self.screen.blit(backgroud_42, (x + WALL_THICKNESS,
                                            y + WALL_THICKNESS))

    def _fill(self, surface: pygame.Surface,
              color: tuple[int, int, int]) -> None:
        x, y = 0, 0
        w, h = surface.get_size()
        pixel_arr = pygame.PixelArray(surface)
        for y in range(h):
            for x in range(w):
                pixel_arr[x, y] = color  # type: ignore

    def quit(self) -> None:
        pygame.quit()
