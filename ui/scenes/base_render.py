import os
import pygame
from abc import ABC
from consts import ANIMATION_FPS
from manager.game import Game
from maze import MazeAdapter


class BaseRender(ABC):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        super().__init__()
        pygame.init()
        pygame.display.set_caption(title)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        win_size_x, win_size_y = win_size
        self._win_size_x = win_size_x
        self._win_size_y = win_size_y
        self._maze = maze
        self._win = pygame.display.set_mode((self._win_size_x,
                                             self._win_size_y),
                                            pygame.NOFRAME)
        self._game = game
        self._animation_fps = 1 / ANIMATION_FPS

    def _render_surface(self, surface: pygame.Surface,
                        pos: tuple[int, int]) -> None:
        self._win.blit(surface, pos)

    def _fill(self, surface: pygame.Surface,
              color: tuple[int, int, int]) -> None:
        pygame.PixelArray(surface)[:] = color  # type: ignore
