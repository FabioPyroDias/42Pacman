import pygame
from maze import MazeAdapter, Cell

Coordinates = tuple[int, int]


WALL_THICKNESS = 5
CELL_SIZE = 50


class GUI:
    def __init__(self, title: str, size: tuple[int, int]) -> None:
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(size)
        self.ns_wall = pygame.Surface((CELL_SIZE, WALL_THICKNESS))
        self.fill(self.ns_wall, (255, 255, 255))
        self.lw_wall = pygame.Surface((WALL_THICKNESS, CELL_SIZE))
        self.fill(self.lw_wall, (255, 255, 255))

    def draw_maze(self, maze: MazeAdapter):
        background = pygame.Surface(self.screen.get_size())
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        for y in range(maze.height):
            for x in range(maze.width):
                self.draw_cell(maze.get_cell(x, y),
                               (x * CELL_SIZE, y * CELL_SIZE))
        pygame.display.update()

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()

    def draw_cell(self, cell: Cell, coord: Coordinates) -> None:
        x, y = coord
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

    def fill(self, surface: pygame.Surface,
             color: tuple[int, int, int]) -> None:
        x, y = 0, 0
        w, h = surface.get_size()
        pixel_arr = pygame.PixelArray(surface)
        for y in range(h):
            for x in range(w):
                pixel_arr[x, y] = color  # type: ignore

    def quit(self) -> None:
        pygame.quit()
