"""Name entry scene rendering."""

import pygame
import time
from manager.game import Game
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    BACKGROUND_COLOR, TEXT_BOX_BACKGROUND_COLOR, COMMOM_TEXT_COLOR,
    CTA_BLINK_INTERVAL
)


class NameEntry(BaseRender):
    """
    Class representing a name entry screen in a game.

    This class is responsible for rendering the name entry interface, handling
    user input for the player's name, and managing the display of various
    text elements on the screen.

    Attributes:
        __player_name (str): The name entered by the player.
        __updated (bool): Flag indicating whether the display has been updated.
        __fonts_loaded (bool): Flag indicating whether the fonts have been
        loaded.
        __text_loaded (bool): Flag indicating whether the text has been loaded.
        _background (pygame.Surface | None): The background surface for the
        name entry screen.
        __blink (bool): Flag for controlling the blinking cursor.
        __last_blink (float): The last time the cursor blink state was updated.

    Methods:
        __update(): Updates the display if the window size has changed.
        __load_fonts(): Loads the necessary fonts for rendering text.
        __load_text(player_name: str): Loads the text elements for the name
        entry screen.
        _render_text_box(): Renders the text box for name entry.
        _render_texts(player_name: str, invalid_name: bool): Renders the
        various text elements on the screen.
        render_name_entry(player_name: str, invalid_name: bool): Main method
        to render the name entry screen.
        handle_name_input(max_len: int, name: str, event: pygame.event.Event)
        -> str: Handles user input for the name entry.
    """
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        """
        Initializes a new instance of the class.

        Args:
            win_size (tuple[int, int]): The size of the window as a tuple
            of width and height.
            title (str): The title of the window.
            game (Game): An instance of the Game class representing the
            current game.
            maze (MazeAdapter): An instance of the MazeAdapter class for
            maze management.

        Attributes:
            __player_name (str): The name of the player.
            __updated (bool): A flag indicating if the state has been updated.
            __fonts_loaded (bool): A flag indicating if the fonts have been
            loaded.
            __text_loaded (bool): A flag indicating if the text has been
            loaded.
            _background (pygame.Surface | None): The background surface for
            the window.
            __blink (bool): A flag for controlling blink state.
            __last_blink (float): The last time the blink state was updated.
        """
        super().__init__(win_size, title, game, maze)
        self.__player_name = ""
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self._background: pygame.Surface | None = None
        self.__blink = True
        self.__last_blink = time.perf_counter()

    def __update(self) -> None:
        """
        Updates the display window and background surfaces.

        This method checks if the current window size is different from the
        expected size of 800x600 pixels. If it is, the window is resized
        without a frame. It also initializes the background and text box
        surfaces, filling them with their respective colors. The method
        ensures that these updates are only performed if they have not
        already been applied.

        Attributes:
            _win (pygame.Surface): The current display window.
            _background (pygame.Surface): The surface for the background.
            _text_box (pygame.Surface): The surface for the text box.
            _win_size_x (int): The width of the window.
            _win_size_y (int): The height of the window.
            __updated (bool): A flag indicating whether the surfaces have been
            updated.

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
        self._text_box = pygame.Surface((self._win_size_x * 0.4,
                                         self._win_size_y * 0.1))
        self._text_box_x, self._text_box_y = self._text_box.get_size()

        self._background.fill(BACKGROUND_COLOR)
        self._text_box.fill(TEXT_BOX_BACKGROUND_COLOR)
        self.__updated = True

    def __load_fonts(self) -> None:
        """
        Loads the necessary fonts for the application.

        This method checks if the fonts have already been loaded.
        If not, it initializes
        the title font, entry font, and hint button font using the
        Pygame library's
        SysFont method. The font sizes are determined based on the
        window size and
        text box height.

        Attributes:
            _name_title_font (pygame.font.Font): The font used for the title.
            _name_entry_font (pygame.font.Font): The font used for text entry.
            _hint_button_font (pygame.font.Font): The font used for hint
            buttons.
            __fonts_loaded (bool): A flag indicating whether the fonts have
            been loaded.
        """
        if self.__fonts_loaded:
            return
        self._name_title_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.15)
        )
        self._name_entry_font = pygame.font.SysFont(
            None,
            int(self._text_box.get_height() * 0.6)
        )
        self._hint_button_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.03)
                    )

        self.__fonts_loaded = True

    def __load_text(self, player_name: str) -> None:
        """
        Loads and renders text elements related to the player's name in the
        game interface.

        This method initializes and updates the text displayed for the
        player's name, title, and instructions.
        It checks if the provided player name is different from the current
        one and updates the rendered text accordingly.
        If the text has already been loaded, it will not reload it.

        Args:
            player_name (str): The name of the player to be displayed. If None
            or different from the current name,
                               the text will be updated.

        Returns:
            None
        """
        self.__load_fonts()
        if not player_name or self.__player_name != player_name:
            self._player_name_text = self._name_entry_font.render(
                player_name,
                0,
                COMMOM_TEXT_COLOR
            )
            self._player_name_rect = self._player_name_text.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        if self.__text_loaded:
            return
        self._name_title = self._name_title_font.render(
            "ENTER YOUR NAME",
            0,
            COMMOM_TEXT_COLOR
        )
        self._underscore = self._name_entry_font.render(
            "_",
            0,
            COMMOM_TEXT_COLOR
        )
        self._back_button_txt = self._hint_button_font.render(
            "<    ESC",
            0,
            COMMOM_TEXT_COLOR
        )
        self._enter_button_txt = self._hint_button_font.render(
            "press ENTER to confirm",
            0,
            COMMOM_TEXT_COLOR
        )
        self._invalid_name_txt = self._name_entry_font.render(
            "Invalid Name",
            0,
            COMMOM_TEXT_COLOR
        )
        self.__text_loaded = True

    def _render_text_box(self) -> None:
        """
        Render a text box onto the window.

        This method blits the text box onto the window at the center of
        the window's dimensions.

        Args:
            None

        Returns:
            None
        """
        self._win.blit(
            self._text_box,
            self._text_box.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2))
        )

    def _render_texts(self, player_name: str, invalid_name: bool) -> None:
        """
        Render the text elements on the game window.

        This method displays various text elements on the game window,
        including the title, back button, enter button, and player name.
        It also handles the display of an invalid name message if the provided
        player name is deemed invalid. Additionally, it manages the blinking
        effect of an underscore character next to the player name.

        Args:
            player_name (str): The name of the player to be displayed.
            invalid_name (bool): A flag indicating whether the player name
            is invalid.

        Returns:
            None
        """
        self._win.blit(
            self._name_title,
            self._name_title.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 6)
                ))
        self._win.blit(
            self._back_button_txt,
            self._back_button_txt.get_rect(
                    center=(self._win_size_x // 20,
                            self._win_size_y // 20)
                            ))
        self._win.blit(
            self._enter_button_txt,
            self._enter_button_txt.get_rect(
                    center=(self._win_size_x // 2,
                            self._win_size_y * 4 // 6)
                            ))
        if invalid_name:
            self._win.blit(
                self._invalid_name_txt,
                self._invalid_name_txt.get_rect(
                    center=(self._win_size_x // 2,
                            self._win_size_y // 2)
                )
            )
            return
        self._win.blit(
            self._player_name_text,
            self._player_name_rect
        )
        if self.__blink:
            if player_name:
                underscore_rect = self._underscore.get_rect(
                    left=self._player_name_rect.right,
                    centery=self._player_name_rect.centery
                    )
            else:
                underscore_rect = self._underscore.get_rect(
                    center=(self._win_size_x // 2, self._win_size_y // 2)
                    )
            self._win.blit(
                self._underscore,
                underscore_rect
            )
        now = time.perf_counter()
        if now - self.__last_blink >= CTA_BLINK_INTERVAL:
            self.__blink = not self.__blink
            self.__last_blink = now

    def render_name_entry(self, player_name: str, invalid_name: bool) -> None:
        """
        Render the name entry for a player.

        This method updates the current state, loads the provided
        player name, and renders
        the background along with the text box and player name.
        It also indicates whether
        the provided name is invalid.

        Args:
            player_name (str): The name of the player to be rendered.
            invalid_name (bool): A flag indicating if the player name
            is invalid.

        Returns:
            None
        """
        self.__update()
        self.__load_text(player_name)
        assert self._background
        self._win.blit(self._background, (0, 0))
        self._render_text_box()
        self._render_texts(player_name, invalid_name)

    def handle_name_input(self, max_len: int, name: str,
                          event: pygame.event.Event) -> str:
        """
        Handles user input for a name field in a pygame application.

        Args:
            max_len (int): The maximum length of the name allowed.
            name (str): The current name input by the user.
            event (pygame.event.Event): The pygame event object
            representing the user input.

        Returns:
            str: The updated name after processing the input event.
            This may include
            the addition of a new character, the removal of the
            last character, or
            the unchanged name if the input does not meet the criteria.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return name[:-1] if name else ''
            letter: str = event.unicode
            if letter.isalnum() or letter == " ":
                return name + letter if len(name) < max_len else name
            elif event.key == pygame.K_RETURN:
                return name
        return name
