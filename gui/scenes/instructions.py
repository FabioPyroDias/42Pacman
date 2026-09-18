"""Instructions scene rendering."""

import pygame
from manager.game import Game
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    COMMOM_TEXT_COLOR, BACKGROUND_COLOR, INSTRUCTIONS_LIST,
    EXPECTECTED_CONTROLS_LEN, CONTROLS_LIST
    )


CONTROLS = [first + "."*abs(
    len(first + second) + 2 - EXPECTECTED_CONTROLS_LEN
    ) + second
    for first, second in CONTROLS_LIST]

INSTRUCTIONS = [first + second
                for first, second in INSTRUCTIONS_LIST]


class Instructions(BaseRender):
    """
    Instructions class for rendering game instructions on the screen.

    This class inherits from BaseRender and is responsible for displaying
    the instructions for the game, including a subtitle, a list of game
    rules (with point/life values substituted from the config), and a
    list of controls.

    Attributes:
        __updated (bool): Indicates whether the background has been updated.
        __fonts_loaded (bool): Indicates whether the fonts have been loaded.
        __text_loaded (bool): Indicates whether the text has been loaded.
        _background (pygame.Surface | None): The background surface for the
        instructions.
        _instructions_list (list[pygame.Surface]): Rendered rule lines, with
        placeholders replaced by config values.
        _controls_list (list[pygame.Surface]): Rendered control/key lines.

    Methods:
        __update(): Updates the background surface if necessary.
        __load_fonts(): Loads the fonts used for rendering text.
        __load_text(): Loads the text to be displayed, including
        instructions, controls, and buttons.
        _subtitle(): Renders the instructions subtitle and back button.
        _render_instructions(): Renders the rule list and the control list
        side by side on the screen.
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
                    int(self._win_size_y * 0.03)
                    )

        self._back_button_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.03)
                    )

        self._intructions_heigth = self._instructions_font.get_linesize()
        self.__fonts_loaded = True

    def __load_text(self) -> None:
        """
        Loads the text elements required for the instructions screen.

        Initializes the fonts, substitutes point/life placeholders
        (`+X`, `+Y`, `+Z`, `+L`) in the rule list with the current game
        config values, and renders the subtitle, back button, rule list
        (`_instructions_list`), and control list (`_controls_list`). Checks
        if the text has already been loaded to avoid redundant operations.

        Attributes:
            _subtitle_instructions: Rendered text for the subtitle
            instructions.
            _back_button_txt: Rendered text for the back button.
            _instructions_list: List of rendered rule texts.
            _controls_list: List of rendered control/key texts.

        Returns:
            None
        """
        instructions = [
            first + second
            for first, second in INSTRUCTIONS_LIST]
        self.__load_fonts()
        if self.__text_loaded:
            return

        instructions = []
        for first, second in INSTRUCTIONS_LIST:
            match first:
                case "Pacgum ":
                    second = second.replace(
                        "+X",
                        str(self._game.config["points_per_pacgum"])
                        )
                case "Super-pacgum ":
                    "points_per_super_pacgum"
                    second = second.replace(
                        "+Y",
                        str(self._game.config["points_per_super_pacgum"])
                        )
                case "Edible Ghost ":
                    second = second.replace(
                        "+Z",
                        str(self._game.config["points_per_ghost"])
                    )
                case "Lives ":
                    second = second.replace(
                        "+L",
                        str(self._game.config["lives"])
                    )
            instructions.append(first + second)

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
                ) for instructions_text in instructions
        ]

        self._controls_list = [
            self._instructions_font.render(
                controls_text,
                0,
                COMMOM_TEXT_COLOR
                ) for controls_text in CONTROLS
        ]

        self.__text_loaded = True

    def _subtitle(self) -> None:
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

    def _render_instructions(self) -> None:
        """
        Render the rule list and the control list on the window.

        Iterates through `_instructions_list` and blits each rule text on
        the left half of the window, and iterates through `_controls_list`,
        blitting each control text on the right half, both positioned
        relative to window size and line height.

        Args:
            None

        Returns:
            None
        """
        for i, instruction_txt in enumerate(self._instructions_list, 1):
            self._win.blit(
                instruction_txt,
                instruction_txt.get_rect(
                    center=(self._win_size_x // 4,
                            self._win_size_y // 4 +
                            (self._intructions_heigth + 10) * i
                            )
                    )
            )
        for i, control_txt in enumerate(self._controls_list, 1):
            self._win.blit(
                control_txt,
                control_txt.get_rect(
                    center=(self._win_size_x * 3 // 4,
                            self._win_size_y // 4 +
                            (self._intructions_heigth + 6) * i
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
        self._subtitle()
        self._render_instructions()
