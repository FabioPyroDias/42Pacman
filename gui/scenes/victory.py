"""Victory scene rendering."""

import pygame
from maze.maze_adapter import MazeAdapter
from manager.game import Game
from .base_render import BaseRender
from consts import (
    VICTORY_TEXT_COLOR
)


class Victory(BaseRender):
    """
    Victory class for rendering a victory screen in a game.

    This class inherits from BaseRender and is responsible for loading fonts,
    rendering victory text, and displaying it on the game window.

    Attributes:
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the victory text has been
        loaded.

    Methods:
        __load_fonts():
            Loads the victory font if it has not been loaded already.

        __load_text():
            Loads the victory text if it has not been loaded already,
            ensuring that fonts are loaded first.

        _render_victory():
            Renders the victory text onto the game window.

        render_victory():
            Public method to load the text and render the victory screen.

    Args:
        win_size (tuple[int, int]): The size of the game window.
        title (str): The title of the game window.
        game (Game): The game instance.
        maze (MazeAdapter): The maze adapter instance.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initializes a new instance of the class.

        Args:
            win_size (tuple[int, int]): A tuple representing the width and
            height of the window.
            title (str): The title of the window.
            game (Game): An instance of the Game class.
            maze (MazeAdapter): An instance of the MazeAdapter class.

        Attributes:
            __fonts_loaded (bool): Indicates whether the fonts have been
            loaded.
            __text_loaded (bool): Indicates whether the text has been loaded.
        """
        super().__init__(win_size, title, game, maze)
        self.__fonts_loaded = False
        self.__text_loaded = False

    def __load_fonts(self) -> None:
        """
        Loads the necessary fonts for the application.

        This method checks if the fonts have already been loaded. If not,
        it initializes
        the victory font using the system font with a size based on the
        window's height.
        Once the fonts are loaded, it sets a flag to indicate that the
        fonts have been
        successfully loaded.

        Returns:
            None
        """
        if self.__fonts_loaded:
            return

        self._victory_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.1)
        )
        self.__fonts_loaded = True

    def __load_text(self) -> None:
        """
        Loads the victory text and renders it using the specified font.

        This method checks if the text has already been loaded. If not,
        it renders
        the victory text "CONGRATULATIONS!!!" using the victory font and
        sets the
        text loaded flag to True.

        Returns:
            None
        """
        self.__load_fonts()
        if self.__text_loaded:
            return

        self._victory_text = self._victory_font.render(
            "CONGRATULATIONS!!!",
            0,
            VICTORY_TEXT_COLOR
        )
        self.__text_loaded = True

    def _render_victory(self) -> None:
        """
        Render the victory text on the window.

        This method blits the victory text onto the window at the
        center of the screen.

        Args:
            None

        Returns:
            None
        """
        self._win.blit(
            self._victory_text,
            self._victory_text.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def render_victory(self) -> None:
        """
        Render the victory screen.

        This method loads the necessary text and then renders the
        victory screen.
        It is typically called when the player has achieved a
        victory in the game.

        Returns:
            None
        """
        self.__load_text()
        self._render_victory()
