import pygame
from .base_render import BaseRender
from entities import Pacman, Ghost, Collectable
from maze import MazeAdapter
from enums import GameState
from consts import (
    COMMOM_TEXT_COLOR
)


class PauseMenu(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 pacman: Pacman, ghosts: list[Ghost],
                 collectables: dict[tuple[int, int], Collectable],
                 game_state: GameState, maze: MazeAdapter, *args) -> None:
        super().__init__(win_size, title, pacman, ghosts,
                         collectables, game_state, maze, *args)
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False

    def __update(self) -> None:
        if self.__updated:
            return
        self._pause_backgroud = pygame.Surface((self._win_size_x * 0.3,
                                                self._win_size_y * 0.1))

        self._pause_size_x = self._pause_backgroud.get_width()
        self._pause_size_y = self._pause_backgroud.get_height()

        self.__updated = True

    def __load_fonts(self) -> None:
        if self.__fonts_loaded:
            return
        self._pause_title_font = pygame.font.SysFont(
            None,
            int(self._pause_size_x * 0.3)
            )
        self.__fonts_loaded = True

    def __load_texts(self) -> None:
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
        self._pause_backgroud.blit(
            self._pause_title,
            self._pause_title.get_rect(
                center=(self._pause_size_x // 2,
                        self._pause_size_y // 2)
            )
        )

    def render_pause(self) -> None:
        self.__update()
        self.__load_texts()
        self._win.blit(
            self._pause_backgroud,
            self._pause_backgroud.get_rect(
                center=(self._win_size_x // 2, self._win_size_y // 2)
                ))
        self._render_pause_text()
