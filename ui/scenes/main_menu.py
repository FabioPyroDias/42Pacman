import pygame
import time

from entities.collectable import Collectable
from entities.ghost import Ghost
from entities.pacman import Pacman
from enums import GameState
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    COMMOM_TEXT_COLOR, GAME_TITLE_COLOR, FOOTER_MARGIN_BOTTOM,
    CTA_BLINK_INTERVAL, BACKGROUND_COLOR
    )


class MainMenu(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 pacman: Pacman, ghosts: list[Ghost],
                 collectables: dict[tuple[int, int], Collectable],
                 game_state: GameState, maze: MazeAdapter, *args) -> None:
        super().__init__(win_size, title, pacman, ghosts,
                         collectables, game_state, maze, *args)
        self.__blink_cta = True
        self.__fonts_loaded = False
        self.__text_loaded = False
        self.__updated = False
        self.__last_blink = time.perf_counter()

    def __load_font(self) -> None:
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
            "H. Highscores  I. Instructions  ESC. Exit",
            0,
            COMMOM_TEXT_COLOR
            )

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

        self._fill(self._background, BACKGROUND_COLOR)

        self.__updated = True

    def _render_tile(self) -> None:
        self._win.blit(
            self._game_title,
            self._game_title.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 6)
                        ))

    def _render_footer(self) -> None:
        self._win.blit(
            self._footer_text,
            self._footer_text.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y - FOOTER_MARGIN_BOTTOM)
                        ))

    def _render_cta(self) -> None:
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
        self.__update()
        self.__load_text()
        self._win.blit(self._background, (0, 0))
        self._render_tile()
        self._render_cta()
        self._render_footer()
