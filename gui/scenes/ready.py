"""Ready countdown scene rendering."""

import pygame
import time
from manager.game import Game
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    READY_COLOR, NUMBERS_COLOR, GO_COLOR,
    READY_STEP_DURATION, CELL_SIZE, MIN_MAZE_SIZE_FOR_42
)


class Ready(BaseRender):
    """
    Ready class for rendering the "Ready" screen in a game.

    This class inherits from BaseRender and is responsible for displaying
    the countdown and "GO!!!" message before the game starts.

    Attributes:
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the texts have been loaded.
        _ready_font (Font): The font used for rendering the "READY!" text and
        countdown numbers.
        _ready_txt (Surface): The rendered "READY!" text.
        _1_txt (Surface): The rendered "1" text.
        _2_txt (Surface): The rendered "2" text.
        _3_txt (Surface): The rendered "3" text.
        _go_txt (Surface): The rendered "GO!!!" text.

    Methods:
        __load_fonts(): Loads the necessary fonts for rendering text.
        __load_texts(): Loads the texts to be rendered on the screen.
        _render_ready(): Renders the "READY!" text on the screen.
        _render_number(start_time: float, now: float): Renders the countdown
        numbers based on the elapsed time.
        _render_go(): Renders the "GO!!!" text on the screen.
        render_ready(start_time: float): Main method to render the ready
        screen, including the countdown and "GO!!!" message.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initializes a new instance of the class.

        Args:
            win_size (tuple[int, int]): A tuple representing the width and
            height of the window.
            title (str): The title of the window.
            game (Game): An instance of the Game class representing the game
            logic.
            maze (MazeAdapter): An instance of the MazeAdapter class for maze
            representation.

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

        This method checks if the fonts have already been loaded. If not, it
        initializes the
        default font using the system font with a size based on the window's
        height.
        Once the fonts are loaded, it sets a flag to indicate that the fonts
        are ready for use.

        Returns:
            None
        """
        if self.__fonts_loaded:
            return
        self._ready_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.14)
            )
        self.__fonts_loaded = True

    def __load_texts(self) -> None:
        """
        Loads the text elements required for the game display.

        This method initializes the text elements used in the game,
        including the
        "READY!" message, countdown numbers (3, 2, 1), and the "GO!!!" message.
        It first ensures that the necessary fonts are loaded and checks if the
        texts have already been loaded to avoid redundant processing.

        Attributes:
            _ready_txt: The rendered text for the "READY!" message.
            _3_txt: The rendered text for the number "3".
            _2_txt: The rendered text for the number "2".
            _1_txt: The rendered text for the number "1".
            _go_txt: The rendered text for the "GO!!!" message.

        Returns:
            None
        """
        self.__load_fonts()
        if self.__text_loaded:
            return
        self._ready_txt = self._ready_font.render(
            "READY!",
            0,
            READY_COLOR
        )
        self._3_txt = self._ready_font.render(
            "3",
            0,
            NUMBERS_COLOR
        )
        self._2_txt = self._ready_font.render(
            "2",
            0,
            NUMBERS_COLOR

        )
        self._1_txt = self._ready_font.render(
            "1",
            0,
            NUMBERS_COLOR
        )
        self._go_txt = self._ready_font.render(
            "GO!!!",
            0,
            GO_COLOR
        )
        self.__text_loaded = True

    def _render_ready(self) -> None:
        """
        Render the 'ready' text on the window.

        This method blits the 'ready' text onto the window at the center
        of the screen,
        using the dimensions of the window to calculate the appropriate
        position.

        Args:
            None

        Returns:
            None
        """
        self._win.blit(
            self._ready_txt,
            self._ready_txt.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def _render_number(self, start_time: float, now: float) -> None:
        """
        Render the countdown number on the window.

        This method calculates the position for rendering a countdown
        number based on the current time and the start time.
        It adjusts the position based on the maze size and blits the
        appropriate text to the window depending on the elapsed time since
        the start.

        Args:
            start_time (float): The time when the countdown started.
            now (float): The current time.

        Returns:
            None
        """
        maze_x, maze_y = self.maze.get_size()
        pos_x = self._win_size_x // 2
        pos_y = self._win_size_y // 2
        if maze_x >= MIN_MAZE_SIZE_FOR_42 and maze_y >= MIN_MAZE_SIZE_FOR_42:
            pos_x = self._win_size_x // 2 - CELL_SIZE // 2
            pos_y = self._win_size_y // 2
        if now - start_time >= READY_STEP_DURATION * 4:
            self._win.blit(
                self._1_txt,
                self._1_txt.get_rect(
                    center=(pos_x, pos_y)
                )
            )
        elif now - start_time >= READY_STEP_DURATION * 3:
            self._win.blit(
                self._2_txt,
                self._2_txt.get_rect(
                    center=(pos_x, pos_y)
                )
            )
        elif now - start_time >= READY_STEP_DURATION * 2:
            self._win.blit(
                self._3_txt,
                self._3_txt.get_rect(
                    center=(pos_x, pos_y)
                )
            )

    def _render_go(self) -> None:
        """
        Render the 'Go' text onto the window.

        This method blits the 'Go' text onto the window at the center
        of the screen.

        Attributes:
            _win: The window surface where the text will be rendered.
            _go_txt: The text surface that contains the 'Go' text.
            _win_size_x: The width of the window.
            _win_size_y: The height of the window.
        """
        self._win.blit(
            self._go_txt,
            self._go_txt.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def render_ready(self, start_time: float) -> None:
        """
        Render the readiness state based on the elapsed time since the start.

        This method checks the elapsed time since the provided start time and
        renders the appropriate state (ready, number, or go) based on
        predefined
        duration thresholds.

        Args:
            start_time (float): The time at which the rendering process
            started, measured in seconds since a reference point.

        Returns:
            None
        """
        self.__load_texts()
        now = time.perf_counter()
        if now - start_time <= READY_STEP_DURATION:
            self._render_ready()
        elif now - start_time <= READY_STEP_DURATION * 5:
            self._render_number(start_time, now)
        elif now - start_time <= READY_STEP_DURATION * 6:
            self._render_go()
