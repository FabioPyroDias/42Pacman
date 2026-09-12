import pygame
from maze.maze_adapter import MazeAdapter
from manager.game import Game
from .base_render import BaseRender
from consts import (
    VICTORY_TEXT_COLOR
)


class Victory(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        super().__init__(win_size, title, game, maze)
        self.__fonts_loaded = False
        self.__text_loaded = False

    def __load_fonts(self) -> None:
        if self.__fonts_loaded:
            return

        self._victory_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.14)
        )
        self.__fonts_loaded = True

    def __load_text(self) -> None:
        self.__load_fonts()
        if self.__text_loaded:
            return

        self._victory_text = self._victory_font.render(
            "VICTORY!!!",
            0,
            VICTORY_TEXT_COLOR
        )
        self.__text_loaded = True

    def _render_victory(self) -> None:
        self._win.blit(
            self._victory_text,
            self._victory_text.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def render_victory(self) -> None:
        self.__load_text()
        self._render_victory()
