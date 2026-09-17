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
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        super().__init__(win_size, title, game, maze)
        self.__player_name = ""
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self._background: pygame.Surface | None = None
        self.__blink = True
        self.__last_blink = time.perf_counter()

    def __update(self) -> None:
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
        self._win.blit(
            self._text_box,
            self._text_box.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2))
        )

    def _render_texts(self, player_name: str, invalid_name: bool) -> None:
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
        self.__update()
        self.__load_text(player_name)
        assert self._background
        self._win.blit(self._background, (0, 0))
        self._render_text_box()
        self._render_texts(player_name, invalid_name)

    def handle_name_input(self, max_len: int, name: str,
                          event: pygame.event.Event) -> str:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return name[:-1] if name else ''
            letter: str = event.unicode
            if letter.isalnum() or letter == " ":
                return name + letter if len(name) < max_len else name
            elif event.key == pygame.K_RETURN:
                return name
        return name
