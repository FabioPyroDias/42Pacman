"""Base rendering utilities for GUI scenes."""

import os
import pygame
from abc import ABC
from consts import ANIMATION_FPS, CELL_SIZE
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
        self.maze = maze
        x, y = maze.get_size()
        self._map_size_x = x * CELL_SIZE
        self._map_size_y = y * CELL_SIZE
        self._last_maze = maze.maze
        self._win = pygame.display.set_mode((self._win_size_x,
                                             self._win_size_y),
                                            pygame.NOFRAME)
        self._game = game
        self._animation_fps = 1 / ANIMATION_FPS

    def _render_surface(self, surface: pygame.Surface,
                        pos: tuple[int, int]) -> None:
        self._win.blit(surface, pos)
