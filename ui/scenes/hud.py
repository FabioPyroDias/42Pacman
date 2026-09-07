import pygame
from .base_render import BaseRender
from game import GameState
from consts import (
    CELL_SIZE, LIFE_ICON_SPRITE_PATH, WALL_OFFSET,
    LIFE_ICON_SPACING, COMMOM_TEXT_COLOR, MAX_SCORE_DIGITS
)


class HUD(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game_state: GameState) -> None:
        super().__init__(win_size, title, game_state)
        self.__assets_loaded = False
        self.__fonts_loaded = False
        self.__text_loaded = False
        self.__current_level = -1
        self.__current_score = -1

    def __load_assets(self) -> None:
        if self.__assets_loaded:
            return
        self._life = pygame.image.load(LIFE_ICON_SPRITE_PATH)

        self.__assets_loaded = True

    def __load_fonts(self) -> None:
        if self.__fonts_loaded:
            return
        self._subtitle_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.05)
            )
        self._text_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.03)
            )

        self.__fonts_loaded = True

    def __load_text(self) -> None:
        self.__load_fonts()
        if self.__current_level != self._game_state.level:
            self._level_title = self._subtitle_font.render(
                f"LEVEL {self._game_state.level}",
                0,
                COMMOM_TEXT_COLOR
            )
        if self.__current_score != self._game_state.score:
            score = str(self._game_state.score)
            if len(score) >= MAX_SCORE_DIGITS:
                score = f"{self._game_state.score:.2e}"
            self._score_text = self._text_font.render(
                score,
                0,
                COMMOM_TEXT_COLOR
            )
        if self.__text_loaded:
            return
        self._score_title = self._text_font.render(
            "SCORE",
            0,
            COMMOM_TEXT_COLOR
            )

        self.__text_loaded = True

    def _render_level_title(self) -> None:
        self._win.blit(self._level_title, self._level_title.get_rect(
            center=(self._win_size_x // 2, CELL_SIZE // 2)
            ))

    def _render_score(self) -> None:
        self._win.blit(
            self._score_title,
            self._score_title.get_rect(
                center=(self._win_size_x // 10, CELL_SIZE // 4)
            )
        )
        self._win.blit(
            self._score_text,
            self._score_text.get_rect(
                center=(self._win_size_x // 10, CELL_SIZE * 5 // 7))
        )

    def _render_life(self) -> None:
        for i in range(self._game_state.life):
            self._render_surface(
                self._life,
                (i * LIFE_ICON_SPACING,
                 self._win_size_y - CELL_SIZE + WALL_OFFSET
                 )
                 )

    def render_hud(self) -> None:
        self.__load_assets()
        self.__load_text()
        self._render_life()
        self._render_level_title()
        self._render_score()
