import pygame
from game import GameState
from .base_render import BaseRender
from consts import (
    GAME_OVER_TEXT_COLOR
)


class GameOver(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game_state: GameState) -> None:
        super().__init__(win_size, title, game_state)
        self.__fonts_loaded = False
        self.__text_loaded = False

    def __load_fonts(self) -> None:
        if self.__fonts_loaded:
            return

        self._game_over_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.14)
        )
        self.__fonts_loaded = True

    def __load_text(self) -> None:
        self.__load_fonts()
        if self.__text_loaded:
            return

        self._game_over_text = self._game_over_font.render(
            "GAME-OVER",
            0,
            GAME_OVER_TEXT_COLOR
        )
        self.__text_loaded = True

    def _render_game_over(self) -> None:
        self._win.blit(
            self._game_over_text,
            self._game_over_text.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def render_game_over(self) -> None:
        self.__load_text()
        self._render_game_over()
