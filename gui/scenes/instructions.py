"""Instructions scene rendering."""

import pygame
from manager.game import Game
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    COMMOM_TEXT_COLOR, BACKGROUND_COLOR, INSTRUCTIONS_LIST,
    EXPECTECTED_INSTRUCTIONS_LEN
    )


INSTRUCTIONS = [first + "."*abs(
    len(first + second) + 2 - EXPECTECTED_INSTRUCTIONS_LEN
    ) + second
    for first, second in INSTRUCTIONS_LIST]


class Instructions(BaseRender):
    """
    Instructions class for rendering game instructions on the screen.

    This class inherits from BaseRender and is responsible for displaying
    the instructions for the game, including a subtitle and a list of
    commands. It handles loading fonts and text, updating the background,
    and rendering the instructions on the game window.

    Attributes:
        __updated (bool): Indicates whether the background has been updated.
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the text has been loaded.
        _background (pygame.Surface | None): The background surface for the
        instructions.

    Methods:
        __update(): Updates the background surface if necessary.
        __load_fonts(): Loads the fonts used for rendering text.
        __load_text(): Loads the text to be displayed, including instructions
        and buttons.
        _render_instructions_subtitle(): Renders the instructions subtitle and
        back button.
        _render_commands(): Renders the list of commands on the screen.
        render_instructions(): Main method to render the instructions on the
        game window.

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
            win_size (tuple[int, int]): The size of the window as a tuple of
            (width, height).
            title (str): The title of the window.
            game (Game): An instance of the Game class representing the game
            logic.
            maze (MazeAdapter): An instance of the MazeAdapter class for maze
            handling.

        Attributes:
            __updated (bool): Indicates whether the instance has been updated.
            __fonts_loaded (bool): Indicates whether the fonts have been
            loaded.
            __text_loaded (bool): Indicates whether the text has been loaded.
            _background (pygame.Surface | None): The background surface for
            the window, or None if not set.
        """
        super().__init__(win_size, title, game, maze)
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self._background: pygame.Surface | None = None

    def __update(self) -> None:
        """
        Updates the background surface of the window if necessary.

        This method checks if the background surface needs to be updated based
        on
        the current window size. If the background surface exists and its size
        does not match the window size, it marks the background as needing an
        update. If the background has already been updated, the method returns
        early. Otherwise, it creates a new background surface with the current
        window size, fills it with the specified background color, and marks
        the update as complete.

        Returns:
            None
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
        Loads the necessary fonts for the application if they have not been
        loaded already.

        This method initializes the subtitle, instructions, and back button
        fonts using the
        Pygame library, scaling their sizes based on the window's height.
        It also sets a flag
        to indicate that the fonts have been loaded to prevent reloading.

        Attributes:
            _subtitle_font (pygame.font.Font): The font used for subtitles.
            _instructions_font (pygame.font.Font): The font used for
            instructions.
            _back_button_font (pygame.font.Font): The font used for the back
            button.
            _instructions_height (int): The height of the instructions font in
            pixels.
            __fonts_loaded (bool): A flag indicating whether the fonts have
            been loaded.

        Returns:
            None
        """
        if self.__fonts_loaded:
            return
        self._subtitle_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.15)
            )
        self._instructions_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.05)
                    )

        self._back_button_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.03)
                    )

        self._intructions_heigth = self._instructions_font.get_linesize()
        self.__fonts_loaded = True

    def __load_text(self) -> None:
        """
        Loads the text elements required for the application.

        This method initializes the fonts and renders the necessary text
        components,
        including the instructions and back button text. It checks if the text
        has
        already been loaded to avoid redundant operations.

        Attributes:
            _subtitle_instructions: Rendered text for the subtitle
            instructions.
            _back_button_txt: Rendered text for the back button.
            _instructions_list: List of rendered instruction texts.

        Returns:
            None
        """
        self.__load_fonts()
        if self.__text_loaded:
            return

        self._subtitle_instructions = self._subtitle_font.render(
                "INSTRUCTIONS",
                0,
                COMMOM_TEXT_COLOR
                )

        self._back_button_txt = self._back_button_font.render(
            "<    ESC",
            0,
            COMMOM_TEXT_COLOR
        )

        self._instructions_list = [
            self._instructions_font.render(
                instructions_text,
                0,
                COMMOM_TEXT_COLOR
                ) for instructions_text in INSTRUCTIONS
        ]

        self.__text_loaded = True

    def _render_instructions_subtitle(self) -> None:
        """
        Render the instructions subtitle and back button text on the window.

        This method blits the subtitle instructions and the back button
        text on top
        the window at specified positions. The subtitle is centered at the top
        of the window, while the back button text is positioned in the top-left
        corner.

        Attributes:
            _win: The window surface where the text will be rendered.
            _subtitle_instructions: The surface containing the subtitle
            instructions text.
            _back_button_txt: The surface containing the back button text.
            _win_size_x: The width of the window.
            _win_size_y: The height of the window.
        """
        self._win.blit(
            self._subtitle_instructions,
            self._subtitle_instructions.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 6)
                ))

        self._win.blit(
            self._back_button_txt,
            self._back_button_txt.get_rect(
                    center=(self._win_size_x // 20,
                            self._win_size_y // 20)
                            ))

    def _render_commands(self) -> None:
        """
        Render the command instructions on the window.

        This method iterates through the list of instructions and blits
        each instruction
        text onto the window at calculated positions based on the window
        size and
        instruction height.

        Args:
            None

        Returns:
            None
        """
        for i, instruction_txt in enumerate(self._instructions_list, 1):
            self._win.blit(
                instruction_txt,
                instruction_txt.get_rect(
                    center=(self._win_size_x // 2,
                            self._win_size_y // 3 +
                            (self._intructions_heigth + 10) * i
                            )
                    )
            )

    def render_instructions(self) -> None:
        """
        Render the instructions on the screen.

        This method updates the necessary components, loads the
        instructional text,
        and then renders the background along with the
        instructions and commands
        onto the window.

        Raises:
            AssertionError: If the background is not set before rendering.
        """
        self.__update()
        self.__load_text()
        assert self._background
        self._win.blit(
            self._background,
            (0, 0)
        )
        self._render_instructions_subtitle()
        self._render_commands()
