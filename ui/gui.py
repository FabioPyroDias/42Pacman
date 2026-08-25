import pygame
from maze import MazeAdapter


WALL_OFFSET = 5


class GUI:
    def __init__(self, title: str, size: tuple[int, int]) -> None:
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(size)

    def draw_maze(self, maze: MazeAdapter):
        background = pygame.Surface(self.screen.get_size())
        background.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))
        NS_path = pygame.Surface((40, 45))
        LW_path = pygame.Surface((45, 40))
        NS_path.fill((0, 0, 0))
        LW_path.fill((0, 0, 0))
        for y in range(maze.height):
            for x in range(maze.width):
                directions = [k for k, v in maze.get_cell(x, y).items()
                              if not v]
                for direction in directions:
                    self.draw_path(direction, NS_path, LW_path,
                                   (x * 50, y * 50))
        pygame.display.update()

    def draw_path(self, direction: str, NS: pygame.Surface,
                  LW: pygame.Surface, cell_pos: tuple[int, int]) -> None:
        x, y = cell_pos
        match direction:
            case "N":
                self.screen.blit(NS, (x + WALL_OFFSET, y))
            case "L":
                self.screen.blit(LW, (x + WALL_OFFSET, y + WALL_OFFSET))
            case "S":
                self.screen.blit(NS, (x + WALL_OFFSET, y + WALL_OFFSET))
            case "W":
                self.screen.blit(LW, (x, y + WALL_OFFSET))
            case _:
                pass

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()

    def quit(self) -> None:
        pygame.quit()
