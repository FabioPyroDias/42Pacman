"""Main menu scene rendering."""

import pygame
import time
from manager.game import Game
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    COMMOM_TEXT_COLOR, GAME_TITLE_COLOR, FOOTER_MARGIN_BOTTOM,
    CTA_BLINK_INTERVAL, BACKGROUND_COLOR
    )


class MainMenu(BaseRender):
    """
    MainMenu class for rendering the main menu of the game.

    This class inherits from BaseRender and is responsible for displaying
    the main menu, including the game title, call-to-action text, and
    footer information. It handles font loading, text rendering, and
    background updates.

    Attributes:
        __blink_cta (bool): Indicates whether the call-to-action text
        should blink.
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the text has been loaded.
        __updated (bool): Indicates whether the window has been updated.
        __last_blink (float): The last time the call-to-action text blinked.
        _background (pygame.Surface | None): The background surface for
        the menu.

    Methods:
        __load_font(): Loads the fonts used for the title and footer text.
        __load_text(): Loads the text for the game title, call-to-action,
        and footer.
        __update(): Updates the window size and background surface if
        necessary.
        _render_tile(): Renders the game title on the window.
        _render_footer(): Renders the footer text on the window.
        _render_cta(): Renders the call-to-action text, blinking it at
        intervals.
        render_menu(): Main method to render the entire menu.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initialize a new instance of the class.

        Args:
            win_size (tuple[int, int]): A tuple representing the width
            and height of the window.
            title (str): The title of the window.
            game (Game): An instance of the Game class representing the
            current game state.
            maze (MazeAdapter): An instance of the MazeAdapter class for
            maze-related functionalities.

        Attributes:
            __blink_cta (bool): A flag indicating whether the call-to-action
            should blink.
            __fonts_loaded (bool): A flag indicating whether the fonts have
            been loaded.
            __text_loaded (bool): A flag indicating whether the text has been
            loaded.
            __updated (bool): A flag indicating whether the instance has been
            updated.
            __last_blink (float): The last time the blink action occurred,
            measured in seconds.
            _background (pygame.Surface | None): The background surface for
            the window, or None if not set.
        """
        super().__init__(win_size, title, game, maze)
        self.__blink_cta = True
        self.__fonts_loaded = False
        self.__text_loaded = False
        self.__updated = False
        self.__last_blink = time.perf_counter()
        self._background: pygame.Surface | None = None

    def __load_font(self) -> None:
        """
        Loads the necessary fonts for the application if they have not
        been loaded already.

        This method initializes the title and footer fonts using the
        Pygame library, setting their sizes based on the window's height.
        It ensures that fonts are only loaded once to optimize performance.

        Attributes:
            _title_font (pygame.font.Font): The font used for the title.
            _footer_font (pygame.font.Font): The font used for the footer.
            __fonts_loaded (bool): A flag indicating whether the fonts have
            been loaded.
        """
        if self.__fonts_loaded:
            return
        self._title_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.15)
            )
        self._footer_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.038)
            )

        self.__fonts_loaded = True

    def __load_text(self) -> None:
        """
        Loads the text elements for the game, including the title
        and footer text.

        This method initializes the game title and footer text by rendering
        them with the specified fonts and colors. It checks if the text has
        already been loaded to avoid redundant operations.

        Attributes:
            _game_title (Surface): The rendered surface for the game title.
            _cta_text (Surface): The rendered surface for the call-to-action
            text.
            _footer_text (Surface): The rendered surface for the footer text.

        Returns:
            None
        """
        self.__load_font()
        if self.__text_loaded:
            return
        self._game_title = self._title_font.render(
            "PAC-MAN",
            0,
            GAME_TITLE_COLOR
            )
        self._cta_text = self._footer_font.render(
                        "press SPACE to start",
                        0,
                        COMMOM_TEXT_COLOR
                        )
        self._footer_text = self._footer_font.render(
            "H. Highscores       I. Instructions        ESC. Exit",
            0,
            COMMOM_TEXT_COLOR
            )

    def __update(self) -> None:
        """
        Updates the window size and background if necessary.

        This method checks if the current window size is different from the
        expected size of 800x600 pixels. If it is, the window is resized
        without a frame. It also creates a background surface filled with a
        specified background color. The method ensures that the background
        is only updated if it has not been updated already.

        Attributes:
            _win (pygame.Surface): The current window surface.
            _win_size_x (int): The width of the window.
            _win_size_y (int): The height of the window.
            __updated (bool): A flag indicating whether the background has
                been updated.

        Returns:
            None
        """
        if self._win.get_size() != (800, 600):
            self._win = pygame.display.set_mode(
                (800, 600),
                pygame.NOFRAME
                    )
            self._win_size_x, self._win_size_y = self._win.get_size()
            self.__updated = False

        if self.__updated:
            return

        self._background = pygame.Surface(self._win.get_size())

        self._background.fill(BACKGROUND_COLOR)

        self.__updated = True

    def _render_tile(self) -> None:
        """
        Render the game title onto the window.

        This method blits the game title onto the window at a position
        determined by the window size. The title is centered horizontally
        and positioned at one-sixth of the window height.

        Args:
            None

        Returns:
            None
        """
        self._win.blit(
            self._game_title,
            self._game_title.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 6)
                        ))

    def _render_footer(self) -> None:
        """
        Render the footer on the window.

        This method blits the footer text onto the window at a position
        centered
        horizontally and aligned to the bottom of the window, with a specified
        margin.

        Args:
            None

        Returns:
            None
        """
        self._win.blit(
            self._footer_text,
            self._footer_text.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y - FOOTER_MARGIN_BOTTOM)
                        ))

    def _render_cta(self) -> None:
        """
        Render the Call to Action (CTA) text on the window.

        This method blits the CTA text onto the window at the
        center of the screen.
        It also handles the blinking effect of the CTA
        text based on a specified
        interval. The blinking state is toggled every
        `CTA_BLINK_INTERVAL` seconds.

        Attributes:
            __blink_cta (bool): Indicates whether the CTA text should be
            blinking.
            __last_blink (float): The last recorded time when the blink state
            was toggled.
            _cta_text (Surface): The text surface to be rendered as the CTA.
            _win (Surface): The window surface where the CTA will be displayed.
            _win_size_x (int): The width of the window.
            _win_size_y (int): The height of the window.

        Returns:
            None
        """
        if self.__blink_cta:
            self._win.blit(
                self._cta_text,
                self._cta_text.get_rect(
                    center=(self._win_size_x // 2,
                            self._win_size_y // 2)
                            ))

        now = time.perf_counter()
        if now - self.__last_blink >= CTA_BLINK_INTERVAL:
            self.__blink_cta = not self.__blink_cta
            self.__last_blink = now

    def render_menu(self) -> None:
        """
        Render the menu on the screen.

        This method updates the menu state, loads the necessary text,
        and renders
        the background, tiles, call-to-action (CTA), and footer components
        of the
        menu.

        Raises:
            AssertionError: If the background is not set before rendering.
        """
        self.__update()
        self.__load_text()
        assert self._background
        self._win.blit(self._background, (0, 0))
        self._render_tile()
        self._render_cta()
        self._render_footer()
