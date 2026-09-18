"""Base rendering utilities for GUI scenes."""

import os
import pygame
from abc import ABC
from consts import ANIMATION_FPS, CELL_SIZE
from manager.game import Game
from maze import MazeAdapter


class BaseRender(ABC):
    """
    BaseRender is an abstract base class for rendering game graphics using
    Pygame.

    Attributes:
        _win_size_x (int): The width of the window in pixels.
        _win_size_y (int): The height of the window in pixels.
        maze (MazeAdapter): An instance of MazeAdapter representing the
        game maze.
        _map_size_x (int): The width of the maze in pixels.
        _map_size_y (int): The height of the maze in pixels.
        _last_maze (list): The last maze configuration.
        _win (pygame.Surface): The Pygame window surface for rendering.
        _game (Game): An instance of the Game class.
        _animation_fps (float): The frame rate for animations.

    Args:
        win_size (tuple[int, int]): The size of the window as (width, height).
        title (str): The title of the window.
        game (Game): An instance of the Game class.
        maze (MazeAdapter): An instance of MazeAdapter representing the
        game maze.

    Methods:
        _render_surface(surface: pygame.Surface, pos: tuple[int, int]) -> None:
            Renders a given surface at the specified position on the window.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initialize a new game window.

        Args:
            win_size (tuple[int, int]): The size of the window as a
            tuple of (width, height).
            title (str): The title of the game window.
            game (Game): An instance of the Game class representing
            the current game.
            maze (MazeAdapter): An instance of the MazeAdapter
            class representing the maze.

        Returns:
            None

        Raises:
            None
        """
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
        """
        Render a surface onto the window at a specified position.

        Args:
            surface (pygame.Surface): The surface to be rendered.
            pos (tuple[int, int]): The (x, y) coordinates where the
            surface will be drawn on the window.

        Returns:
            None
        """
        self._win.blit(surface, pos)
