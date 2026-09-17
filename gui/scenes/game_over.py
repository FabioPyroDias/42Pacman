"""Game over scene rendering."""

import pygame
from manager.game import Game
from maze import MazeAdapter
from .base_render import BaseRender
from consts import (
    GAME_OVER_TEXT_COLOR
)


class GameOver(BaseRender):
    """
    GameOver class for rendering the game over screen.

    This class inherits from BaseRender and is responsible for loading fonts,
    rendering the game over text, and displaying it on the screen when the
    game ends.

    Attributes:
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the game over text has been
        loaded.
        _game_over_font (Font): The font used for the game over text.
        _game_over_text (Surface): The rendered game over text surface.

    Args:
        win_size (tuple[int, int]): The size of the window as a tuple of
        (width, height).
        title (str): The title of the window.
        game (Game): The game instance associated with this render.
        maze (MazeAdapter): The maze adapter instance associated with this
        render.

    Methods:
        __load_fonts(): Loads the game over font if it hasn't been loaded yet.
        __load_text(): Loads the game over text if it hasn't been loaded yet.
        _render_game_over(): Renders the game over text onto the window.
        render_game_over(): Public method to load text and render the game
        over screen.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game,
                 maze: MazeAdapter) -> None:
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
        Loads the game over font if it has not been loaded already.

        This method checks if the fonts have already been loaded. If not,
        it initializes
        the game over font using the system font with a size based on the
        window's
        height. Once the font is loaded, it sets the `__fonts_loaded`
        attribute to True
        to prevent reloading.

        Returns:
            None
        """
        if self.__fonts_loaded:
            return

        self._game_over_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.14)
        )
        self.__fonts_loaded = True

    def __load_text(self) -> None:
        """
        Loads the game over text and renders it using the specified font.

        This method checks if the text has already been loaded. If not,
        it calls
        the font loading method and renders the "GAME-OVER" text using the
        game over font. The rendered text is stored for later use.

        Attributes:
            _game_over_text: The rendered game over text.
            __text_loaded (bool): A flag indicating whether the text has been
            loaded.

        Returns:
            None
        """
        self.__load_fonts()
        if self.__text_loaded:
            return

        self._game_over_text = self._game_over_font.render(
            "GAME-OVER",
            0,
            GAME_OVER_TEXT_COLOR
        )
        self.__text_loaded = True

    def _render_game_over(self) -> None:
        """
        Render the game over screen to the user.

        This method is responsible for displaying the game over screen.
        It calls internal methods to load the necessary text and
        render the screen.

        Returns:
            None
        """
        self._win.blit(
            self._game_over_text,
            self._game_over_text.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def render_game_over(self) -> None:
        """
        Render the game over screen.

        This method is responsible for loading the necessary text and rendering
        the game over screen to the user. It calls the internal methods to
        perform these actions.

        Returns:
            None
        """
        self.__load_text()
        self._render_game_over()
