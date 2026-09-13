import pygame
from manager.game import Game
from maze import MazeAdapter
from .base_render import BaseRender
from consts import (
    BACKGROUND_COLOR, COMMOM_TEXT_COLOR, EXPECTECTED_HIGHSCORES_LEN,
    MAX_SCORE_DIGITS
)


class HighscoreView(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter,
                 **kargs: object) -> None:
        super().__init__(win_size, title, game, maze, **kargs)
        self._highscores: list[dict[str, str | int]] | None = None
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self._background: pygame.Surface | None = None

    def __update(self) -> None:
        if (self._background
                and self._background.get_size() != self._win.get_size()):
            self.__updated = False
        if self.__updated:
            return

        self._background = pygame.Surface(self._win.get_size())

        self._background.fill(BACKGROUND_COLOR)

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

    def __load_text(self, highscores: list[dict[str, str | int]]) -> None:
        self.__load_fonts()
        if self._highscores != highscores:
            self._highscores = highscores
            highscores_list: list[str] = []
            for highscore in self._highscores:
                name = highscore["name"]
                score = highscore["score"]
                assert isinstance(score, int) and isinstance(name, str)
                if len(str(score)) >= MAX_SCORE_DIGITS:
                    highscores_list.append(f"{name} " + "." * abs(
                        len(
                            name + f"{score:.2e}"
                            ) + 2 - EXPECTECTED_HIGHSCORES_LEN
                        ) + f" {score:.2e}")
                else:
                    highscores_list.append(f"{name} " + "." * abs(
                        len(name + f"{score}") + 2 - EXPECTECTED_HIGHSCORES_LEN
                        ) + f" {score}")
            self._highscore_list = [
                self._highscore_font.render(
                    score,
                    0,
                    COMMOM_TEXT_COLOR
                ) for score in highscores_list
            ]
        if self.__text_loaded:
            return
        self._subtitle_highscores = self._subtitle_font.render(
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

        self.__text_loaded = True

    def _render_highscores_subtitle(self) -> None:
        self._win.blit(
            self._subtitle_highscores,
            self._subtitle_highscores.get_rect(
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

    def render_highscores(self, highscore: list[dict[str, str | int]]) -> None:
        self.__update()
        self.__load_text(highscore)
        assert self._background
        self._win.blit(
            self._background,
            (0, 0)
        )
        self._render_highscores_subtitle()
        self._render_highscores_text()
