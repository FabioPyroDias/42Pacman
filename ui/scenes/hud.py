import pygame

from entities.collectable import Collectable
from entities.ghost import Ghost
from entities.pacman import Pacman
from enums import GameState
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    CELL_SIZE, LIFE_ICON_SPRITE_PATH, WALL_OFFSET,
    LIFE_ICON_SPACING, COMMOM_TEXT_COLOR, MAX_SCORE_DIGITS
)


class HUD(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 pacman: Pacman, ghosts: list[Ghost],
                 collectables: dict[tuple[int, int], Collectable],
                 game_state: GameState, maze: MazeAdapter, *args) -> None:
        super().__init__(win_size, title, pacman, ghosts,
                         collectables, game_state, maze, *args)
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

    def __load_text(self, level: int, score: int) -> None:
        self.__load_fonts()
        if self.__current_level != level:
            self._level_title = self._subtitle_font.render(
                f"LEVEL {level}",
                0,
                COMMOM_TEXT_COLOR
            )
            self.__current_level = level
        if self.__current_score != score:
            txt_score = str(score)
            if len(txt_score) >= MAX_SCORE_DIGITS:
                txt_score = f"{score:.2e}"
            self._score_text = self._text_font.render(
                txt_score,
                0,
                COMMOM_TEXT_COLOR
            )
            self.__current_score = score
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

    def _render_life(self, lives: int) -> None:
        for i in range(lives):
            self._render_surface(
                self._life,
                (i * LIFE_ICON_SPACING,
                 self._win_size_y - CELL_SIZE + WALL_OFFSET
                 )
                 )

    def render_hud(self, level: int, score: int, lives: int) -> None:
        self.__load_assets()
        self.__load_text(level + 1, score)
        self._render_life(lives)
        self._render_level_title()
        self._render_score()
