"""Pause menu scene rendering."""

import pygame
from .base_render import BaseRender
from manager.game import Game
from maze import MazeAdapter
from consts import (
    COMMOM_TEXT_COLOR
)


class PauseMenu(BaseRender):
    """
    PauseMenu class for rendering a pause menu in a game.

    This class inherits from BaseRender and is responsible for displaying
    the pause menu, including loading fonts and texts, and rendering the
    pause background and title.

    Attributes:
        __updated (bool): Indicates whether the pause menu has been updated.
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the texts have been loaded.
        _pause_backgroud (pygame.Surface): The background surface for the
        pause menu.
        _pause_title_font (pygame.font.Font): The font used for the pause
        title.
        _pause_title (pygame.Surface): The rendered text surface for the pause
        title.
        _pause_size_x (int): The width of the pause background.
        _pause_size_y (int): The height of the pause background.

    Args:
        win_size (tuple[int, int]): The size of the window as a tuple
        (width, height).
        title (str): The title of the window.
        game (Game): The game instance.
        maze (MazeAdapter): The maze adapter instance.

    Methods:
        __update(): Updates the pause menu background and dimensions.
        __load_fonts(): Loads the font for the pause title.
        __load_texts(): Loads the text for the pause title.
        _render_pause_text(): Renders the pause title text onto the background.
        render_pause(): Renders the entire pause menu onto the window.
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
            __updated (bool): Indicates whether the instance has been updated.
            __fonts_loaded (bool): Indicates whether the fonts have been
            loaded.
            __text_loaded (bool): Indicates whether the text has been loaded.
        """
        super().__init__(win_size, title, game, maze)
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False

    def __update(self) -> None:
        """
        Updates the pause background surface and its dimensions if not already
        updated.

        This method checks if the update has already been performed. If not,
        it creates a new
        surface for the pause background based on the window size and sets the
        dimensions
        for the pause background. It then marks the update as completed.

        Attributes:
            __updated (bool): A flag indicating whether the update has been
            performed.
            _pause_backgroud (pygame.Surface): The surface used for the pause
            background.
            _pause_size_x (int): The width of the pause background surface.
            _pause_size_y (int): The height of the pause background surface.
        """
        if self.__updated:
            return
        self._pause_backgroud = pygame.Surface((self._win_size_x * 0.3,
                                                self._win_size_y * 0.1))

        self._pause_size_x = self._pause_backgroud.get_width()
        self._pause_size_y = self._pause_backgroud.get_height()

        self.__updated = True

    def __load_fonts(self) -> None:
        """
        Loads the necessary fonts for the application if they have not been
        loaded already.

        This method checks if the fonts have already been loaded. If not, it
        initializes the pause title font using the specified size.
        Once the fonts are loaded, it sets a flag to indicate that the
        fonts are now loaded.

        Attributes:
            _pause_title_font (pygame.font.Font): The font used for the pause
            title.
            _pause_size_x (float): The base size used to calculate the font
            size.
            __fonts_loaded (bool): A flag indicating whether the fonts have
            been loaded.
        """
        if self.__fonts_loaded:
            return
        self._pause_title_font = pygame.font.SysFont(
            None,
            int(self._pause_size_x * 0.3)
            )
        self.__fonts_loaded = True

    def __load_texts(self) -> None:
        """
        Loads the necessary text for the application.

        This method initializes the fonts and renders the "PAUSED" title text
        if it has not been loaded yet.
        It ensures that the text is only loaded once during the application's
        lifecycle.

        Attributes:
            _pause_title (Surface): The rendered surface of the "PAUSED" title.
            __text_loaded (bool): A flag indicating whether the text has been
            loaded.

        Returns:
            None
        """
        self.__load_fonts()
        if self.__text_loaded:
            return
        self._pause_title = self._pause_title_font.render(
            "PAUSED",
            0,
            COMMOM_TEXT_COLOR
        )

        self.__text_loaded = True

    def _render_pause_text(self) -> None:
        """
        Render the pause text on the background.

        This method blits the pause title onto the pause background at the
        center of the specified pause size.

        Args:
            None

        Returns:
            None
        """
        self._pause_backgroud.blit(
            self._pause_title,
            self._pause_title.get_rect(
                center=(self._pause_size_x // 2,
                        self._pause_size_y // 2)
            )
        )

    def render_pause(self) -> None:
        """
        Render the pause screen for the game.

        This method updates the game state, loads the necessary text for the
        pause screen,
        and then draws the pause background and text onto the window.

        Attributes:
            _win: The window surface where the pause screen will be rendered.
            _pause_background: The background image for the pause screen.
            _win_size_x: The width of the window.
            _win_size_y: The height of the window.

        Returns:
            None
        """
        self.__update()
        self.__load_texts()
        self._win.blit(
            self._pause_backgroud,
            self._pause_backgroud.get_rect(
                center=(self._win_size_x // 2, self._win_size_y // 2)
                ))
        self._render_pause_text()
