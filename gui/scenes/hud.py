"""HUD scene rendering and status overlays."""

import pygame
from manager.game import Game
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from enums import GameState
from consts import (
    CELL_SIZE, LIFE_ICON_SPRITE_PATH, SPRITE_SIZE, WALL_OFFSET,
    LIFE_ICON_SPACING, COMMOM_TEXT_COLOR, MAX_SCORE_DIGITS
)


class HUD(BaseRender):
    """
    HUD class for rendering the Heads-Up Display (HUD) in a game.

    This class is responsible for loading and rendering various HUD elements
    such as the level title, score, timer, and life icons. It inherits from
    the BaseRender class and utilizes Pygame for graphical rendering.

    Attributes:
        __assets_loaded (bool): Indicates whether the assets have been loaded.
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the text has been loaded.
        __current_level (int): The current level being displayed.
        __current_score (int): The current score being displayed.
        __last_size (tuple[int, int]): The last known size of the window.

    Methods:
        __load_assets(): Loads the necessary assets for the HUD.
        __load_fonts(): Loads the fonts used for rendering text in the HUD.
        __load_text(level: int, score: int): Loads the text for the current
        level and score.
        _render_level_title(): Renders the current level title on the screen.
        _render_score(): Renders the current score on the screen.
        _render_timer(time: float): Renders the timer on the screen.
        _render_life(lives: int): Renders the life icons on the screen.
        render_hud(level: int, score: int, lives: int, timer: float,
        game_state: GameState): Renders the entire HUD based on the current
        game state.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initialize a new instance of the class.

        Args:
            win_size (tuple[int, int]): The size of the window as a
            tuple of width and height.
            title (str): The title of the window.
            game (Game): An instance of the Game class representing the
            game logic.
            maze (MazeAdapter): An instance of the MazeAdapter class for
            maze handling.

        Attributes:
            __assets_loaded (bool): Indicates whether the game assets have
            been loaded.
            __fonts_loaded (bool): Indicates whether the fonts have been
            loaded.
            __text_loaded (bool): Indicates whether the text has been loaded.
            __current_level (int): The current level of the game, initialized
            to -1.
            __current_score (int): The current score of the player,
            initialized to -1.
            __last_size (tuple[int, int]): The last known size of the window,
            initialized to (0, 0).
        """
        super().__init__(win_size, title, game, maze)
        self.__assets_loaded = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self.__current_level = -1
        self.__current_score = -1
        self.__last_size = (0, 0)
        self.__current_lives = -1

    def __load_assets(self) -> None:
        """
        Loads the necessary assets for the game if they have not already been
        loaded.

        This method checks if the assets have already been loaded. If not, it
        loads the life icon sprite from the specified path and marks the
        assets as loaded.

        Attributes:
            __assets_loaded (bool): A flag indicating whether the assets have
            been loaded.
            _life (Surface): The loaded life icon sprite.

        Returns:
            None
        """
        if self.__assets_loaded:
            return
        self._life = pygame.image.load(LIFE_ICON_SPRITE_PATH)

        self.__assets_loaded = True

    def __load_fonts(self) -> None:
        """
        Loads the fonts required for rendering subtitles and text.

        This method checks if the fonts have already been loaded.
        If not, it initializes
        the subtitle and text fonts using the Pygame library, setting
        their sizes
        relative to the window's height. Once the fonts are loaded,
        it updates the
        internal state to indicate that the fonts have been successfully
        loaded.

        Attributes:
            _subtitle_font (pygame.font.Font): The font object used for
            subtitles.
            _text_font (pygame.font.Font): The font object used for general
            text.
            __fonts_loaded (bool): A flag indicating whether the fonts have
            been loaded.
            _win_size_y (int): The height of the window used to calculate font
            sizes.

        Returns:
            None
        """
        if self.__fonts_loaded:
            return
        self._subtitle_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.05)
            )
        self._text_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.03)
            )
        self._live_font = pygame.font.SysFont(
            None,
            SPRITE_SIZE
        )

        self.__fonts_loaded = True

    def __load_text(self, level: int, score: int) -> None:
        """
        Loads and updates the text displayed on the screen based
        on the current game level and score.

        This method checks if the window size has changed and reloads
        fonts if necessary. It updates the level title and score text
        if they have changed since the last update. Additionally, it
        ensures that the score and timer titles are rendered only once
        per session.

        Args:
            level (int): The current game level to display.
            score (int): The current score to display.

        Returns:
            None
        """
        if self.__last_size != self._win.get_size():
            self.__last_size = self._win.get_size()
            self.__fonts_loaded = False
            self.__text_loaded = False
        self.__load_fonts()
        if self.__current_level != level:
            self._level_title = self._subtitle_font.render(
                f"LEVEL {level}",
                0,
                COMMOM_TEXT_COLOR
            )
            self.__current_level = level
        if (self._game.lives != self.__current_lives):
            self.__current_lives = self._game.lives
            self._live_text = self._live_font.render(
                f"+{self._game.lives - 3}",
                0,
                COMMOM_TEXT_COLOR
            )
        if self.__current_score != score or not self.__text_loaded:
            txt_score = str(score)
            if len(txt_score) >= MAX_SCORE_DIGITS:
                txt_score = f"{score:.2e}"
            self._score_text = self._text_font.render(
                txt_score,
                0,
                COMMOM_TEXT_COLOR
            )
            self.__current_score = score
        if self.__text_loaded:
            return
        self._score_title = self._text_font.render(
            "SCORE",
            0,
            COMMOM_TEXT_COLOR
            )
        self._timer_title = self._text_font.render(
            "TIME",
            0,
            COMMOM_TEXT_COLOR
        )

        self.__text_loaded = True

    def _render_level_title(self) -> None:
        """
        Render the level title on the window.

        This method blits the level title onto the window at a
        position centered
        horizontally and vertically based on the window size and a
        predefined cell size.

        Args:
            None

        Returns:
            None
        """
        self._win.blit(
            self._level_title,
            self._level_title.get_rect(
                center=(self._win_size_x // 2, CELL_SIZE // 2)
            ))

    def _render_score(self) -> None:
        """
        Render the score title and score text on the game window.

        This method blits the score title and score text onto the window
        at specified positions.
        The score title is centered at a position determined by the window
        size and a constant
        CELL_SIZE, while the score text is positioned slightly lower.

        Attributes:
            _win: The game window where the score will be rendered.
            _score_title: The title of the score to be displayed.
            _score_text: The current score to be displayed.
            _win_size_x: The width of the game window.
            CELL_SIZE: A constant representing the size of a cell in the
            game grid.

        Returns:
            None
        """
        self._win.blit(
            self._score_title,
            self._score_title.get_rect(
                center=(self._win_size_x // 10, CELL_SIZE // 4)
            )
        )
        self._win.blit(
            self._score_text,
            self._score_text.get_rect(
                center=(self._win_size_x // 10, CELL_SIZE * 5 // 7))
        )

    def _render_timer(self, time: float) -> None:
        """
        Render the timer on the game window.

        This method displays the timer title and the formatted time on
        the game window.
        The time is rounded to two decimal places and displayed in
        either standard or
        scientific notation depending on its length.

        Args:
            time (float): The time value to be displayed on the timer.

        Returns:
            None
        """
        self._win.blit(
            self._timer_title,
            self._timer_title.get_rect(
                center=(self._win_size_x * 9 // 10,
                        (self._win_size_y - CELL_SIZE // 4)
                        - self._text_font.get_height())
            )
        )
        rounded_time = round(time, 2)
        rounded_time_len = len(str(rounded_time))
        if rounded_time_len <= MAX_SCORE_DIGITS:
            time_surface = self._text_font.render(
                f"{rounded_time}",
                0,
                COMMOM_TEXT_COLOR)
        else:
            time_surface = self._text_font.render(
                f"{rounded_time:.2e}",
                0,
                COMMOM_TEXT_COLOR)
        self._win.blit(
                time_surface,
                time_surface.get_rect(
                    center=(self._win_size_x * 9 // 10,
                            self._win_size_y - CELL_SIZE // 4)
                )
                )

    def _render_life(self, lives: int) -> None:
        """
        Render the life icons on the screen.

        This method draws a specified number of life icons,
        on the game surface. The icons are spaced apart according to a
        predefined
        spacing constant and are positioned at a specific location on the
        screen.

        Args:
            lives (int): The number of life icons to render.

        Returns:
            None
        """
        for i in range(lives):
            if i == 3:
                break
            self._render_surface(
                self._life,
                (i * LIFE_ICON_SPACING + WALL_OFFSET,
                 self._win_size_y - CELL_SIZE + WALL_OFFSET
                 )
                 )
        if lives > 3:
            self._win.blit(
                self._live_text,
                self._live_text.get_rect(
                    center=(4 * LIFE_ICON_SPACING + WALL_OFFSET,
                            self._win_size_y - (
                                CELL_SIZE - SPRITE_SIZE // 2 + WALL_OFFSET
                                )
                            )
                )
            )

    def render_hud(self, level: int, score: int,
                   lives: int, timer: float,
                   game_state: GameState) -> None:
        """
        Render the heads-up display (HUD) for the game.

        This method updates and displays the HUD elements including the
        level, score, lives, and timer.
        It adjusts the level displayed based on the current game state,
        loading the appropriate assets
        and rendering the necessary components.

        Args:
            level (int): The current level of the game.
            score (int): The current score of the player.
            lives (int): The number of lives remaining for the player.
            timer (float): The remaining time for the current game session.
            game_state (GameState): The current state of the game, which can
            affect the level displayed.

        Returns:
            None
        """
        self.__load_assets()
        self.__load_text(level if game_state == GameState.VICTORY
                         else level + 1, score)
        self._render_timer(timer)
        self._render_life(lives)
        self._render_level_title()
        self._render_score()
