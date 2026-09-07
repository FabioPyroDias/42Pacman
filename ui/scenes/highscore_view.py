import pygame
from pathlib import Path
import json
from game.game_state import GameState
from .base_render import BaseRender
from consts import (
    BACKGROUND_COLOR, COMMOM_TEXT_COLOR, EXPECTECTED_HIGHSCORES_LEN
)


class HighscoreView(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game_state: GameState) -> None:
        super().__init__(win_size, title, game_state)
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self.__highscore_loaded = False

    def __update(self) -> None:
        if (hasattr(self, "_background")
                and self._background.get_size() != self._win.get_size()):
            self.__updated = False
        if self.__updated:
            return

        self._background = pygame.Surface(self._win.get_size())

        self._fill(self._background, BACKGROUND_COLOR)

        self.__updated = True

    def __load_fonts(self) -> None:
        if self.__fonts_loaded:
            return

        self._subtitle_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.15)
            )
        self._highscore_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.05)
                    )

        self._highscore_heigth = self._highscore_font.get_linesize()
        self.__fonts_loaded = True

    def __load_highscores(self) -> None:
        if self.__highscore_loaded:
            return

        highscores_file = Path(self._game_state.highscore_path)
        if not highscores_file.exists():
            self._highscores = {}
            return

        with open(highscores_file) as file:
            self._highscores = json.load(file)
            print(self._highscores)

        self.__highscore_loaded = True

    def __load_text(self) -> None:
        self.__load_fonts()
        self.__load_highscores()
        if hasattr(self, "_subtitle"):
            self.__text_loaded = False
        if self.__text_loaded:
            return
        self._subtitle = self._subtitle_font.render(
            "HIGHSCORES",
            0,
            COMMOM_TEXT_COLOR
        )
        if not self._highscores:
            self._highscore_list = [
                self._highscore_font.render(
                    "Claim the top spot",
                    0,
                    COMMOM_TEXT_COLOR
                )
            ]
            return
        highscores = [f"{first} " + "." * abs(
            len(first + str(second)) + 2 - EXPECTECTED_HIGHSCORES_LEN
            ) + f" {second}"
            for first, second in self._highscores.items()]
        self._highscore_list = [
            self._highscore_font.render(
                score,
                0,
                COMMOM_TEXT_COLOR
            ) for score in highscores
        ]

        self.__text_loaded = True

    def _render_highscores_subtitle(self) -> None:
        self._win.blit(
            self._subtitle,
            self._subtitle.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 6)
            )
        )

    def _render_highscores_text(self) -> None:
        for i, score in enumerate(self._highscore_list):
            self._win.blit(
                score,
                self._highscore_list[0].get_rect(
                    center=(self._win_size_x // 2,
                            self._win_size_y // 3 +
                            (self._highscore_heigth + 10) * i
                            )
                    )
            )

    def render_highscores(self) -> None:
        self.__update()
        self.__load_text()
        self._win.blit(
            self._background,
            (0, 0)
        )
        self._render_highscores_subtitle()
        self._render_highscores_text()
