"""Highscore scene rendering."""

import pygame
from manager.game import Game
from maze import MazeAdapter
from .base_render import BaseRender
from consts import (
    BACKGROUND_COLOR, COMMOM_TEXT_COLOR, EXPECTECTED_HIGHSCORES_LEN,
    MAX_SCORE_DIGITS
)


class HighscoreView(BaseRender):
    """
    Class representing the high score view in the game.

    This class is responsible for rendering the high score screen, including
    the background and the high score subtitles and text.

    Attributes:
        _win (pygame.Surface): The window surface where the high score view
        is rendered.
        _background (pygame.Surface): The background surface to be displayed.

    Methods:
        _render_highscores_subtitle(): Renders the subtitle for the high
        scores.
        _render_highscores_text(): Renders the actual high scores text.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initializes a new instance of the class.

        Args:
            win_size (tuple[int, int]): The size of the window as a
            tuple of width and height.
            title (str): The title of the window.
            game (Game): An instance of the Game class.
            maze (MazeAdapter): An instance of the MazeAdapter class.

        Returns:
            None
        """
        super().__init__(win_size, title, game, maze)
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self._background: pygame.Surface | None = None

    def __update(self) -> None:
        """
        Updates the display by rendering the background and high scores.

        This method asserts that a background image is set, then
        blits the background
        onto the window. It subsequently calls methods to render
        the high scores
        subtitle and the high scores text.

        Raises:
            AssertionError: If the background is not set.
        """
        if (self._background
                and self._background.get_size() != self._win.get_size()):
            self.__updated = False
        if self.__updated:
            return

        self._background = pygame.Surface(self._win.get_size())

        self._background.fill(BACKGROUND_COLOR)

        self.__updated = True

    def __load_fonts(self) -> None:
        """
        Loads the necessary fonts for the application.

        This method is responsible for updating the application state,
        loading the high score text, and rendering the background and
        high score display. It asserts that the background is properly
        loaded before proceeding with the rendering.

        Raises:
            AssertionError: If the background is not loaded.

        Returns:
            None
        """
        if self.__fonts_loaded:
            return

        self._subtitle_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.15)
            )
        self._highscore_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.05)
                    )
        self._back_button_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.03)
                    )

        self._highscore_heigth = self._highscore_font.get_linesize()
        self.__fonts_loaded = True

    def __load_text(self, highscores: list[dict[str, str | int]]) -> None:
        """
        Loads high score data into the application.

        This method processes a list of high score entries,
        where each entry is represented as a dictionary containing the high
        score information. It updates the display with the current high scores.

        Args:
            highscores (list[dict[str, str | int]]): A list of dictionaries,
            each representing a high score entry with string keys and values
            that can be either strings or integers.

        Returns:
            None
        """
        self.__load_fonts()
        highscores_list: list[str] = []
        for highscore in highscores:
            name = highscore["name"]
            score = highscore["score"]
            assert isinstance(score, int) and isinstance(name, str)
            if len(str(score)) >= MAX_SCORE_DIGITS:
                highscores_list.append(f"{name} " + "." * abs(
                    len(
                        name + f"{score:.2e}"
                        ) + 2 - EXPECTECTED_HIGHSCORES_LEN
                    ) + f" {score:.2e}")
            else:
                highscores_list.append(f"{name} " + "." * abs(
                    len(name + f"{score}") + 2 - EXPECTECTED_HIGHSCORES_LEN
                    ) + f" {score}")
        self._highscore_list = [
            self._highscore_font.render(
                score,
                0,
                COMMOM_TEXT_COLOR
            ) for score in highscores_list
            ]
        if self.__text_loaded:
            return
        self._subtitle_highscores = self._subtitle_font.render(
            "HIGHSCORES",
            0,
            COMMOM_TEXT_COLOR
        )

        self._back_button_txt = self._back_button_font.render(
            "<    ESC",
            0,
            COMMOM_TEXT_COLOR
        )

        if not highscores:
            self._highscore_list = [
                self._highscore_font.render(
                    "Claim the top spot",
                    0,
                    COMMOM_TEXT_COLOR
                )
            ]
            return

        self.__text_loaded = True

    def _render_highscores_subtitle(self) -> None:
        """
        Render the highscores screen's subtitle and back button.

        Blits the "Highscores" subtitle centered near the top of the window,
        and the back-button text near the top-left corner.

        Returns:
            None
        """
        self._win.blit(
            self._subtitle_highscores,
            self._subtitle_highscores.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 6)
            )
        )

        self._win.blit(
            self._back_button_txt,
            self._back_button_txt.get_rect(
                    center=(self._win_size_x // 20,
                            self._win_size_y // 20)
                            ))

    def _render_highscores_text(self) -> None:
        """
        Render the list of highscore entries.

        Blits each pre-rendered highscore surface onto the window, stacked
        vertically and centered horizontally, starting below the subtitle.

        Returns:
            None
        """
        for i, score in enumerate(self._highscore_list):
            self._win.blit(
                score,
                self._highscore_list[0].get_rect(
                    center=(self._win_size_x // 2,
                            self._win_size_y // 3 +
                            (self._highscore_heigth + 10) * i
                            )
                    )
            )

    def render_highscores(self, highscore: list[dict[str, str | int]]) -> None:
        """
        Render the high scores on the screen.

        This method updates the current state, loads the high score text,
        and renders
        the background along with the high scores subtitle and text.

        Args:
            highscore (list[dict[str, str | int]]): A list of
            dictionaries containing
            high score data, where each dictionary represents a high
            score entry.

        Returns:
            None
        """
        self.__update()
        self.__load_text(highscore)
        assert self._background
        self._win.blit(
            self._background,
            (0, 0)
        )
        self._render_highscores_subtitle()
        self._render_highscores_text()
