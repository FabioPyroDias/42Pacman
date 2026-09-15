import pygame
import time
from manager.game import Game
from maze.maze_adapter import MazeAdapter
from .base_render import BaseRender
from consts import (
    READY_COLOR, NUMBERS_COLOR, GO_COLOR,
    READY_STEP_DURATION, CELL_SIZE
)


class Ready(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        super().__init__(win_size, title, game, maze)
        self.__fonts_loaded = False
        self.__text_loaded = False

    def __load_fonts(self) -> None:
        if self.__fonts_loaded:
            return
        self._ready_font = pygame.font.SysFont(
            None,
            int(self._win_size_y * 0.14)
            )
        self.__fonts_loaded = True

    def __load_texts(self) -> None:
        self.__load_fonts()
        if self.__text_loaded:
            return
        self._ready_txt = self._ready_font.render(
            "READY!",
            0,
            READY_COLOR
        )
        self._3_txt = self._ready_font.render(
            "3",
            0,
            NUMBERS_COLOR
        )
        self._2_txt = self._ready_font.render(
            "2",
            0,
            NUMBERS_COLOR

        )
        self._1_txt = self._ready_font.render(
            "1",
            0,
            NUMBERS_COLOR
        )
        self._go_txt = self._ready_font.render(
            "GO!!!",
            0,
            GO_COLOR
        )
        self.__text_loaded = True

    def _render_ready(self) -> None:
        self._win.blit(
            self._ready_txt,
            self._ready_txt.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def _render_number(self, start_time: float, now: float) -> None:
        if now - start_time >= READY_STEP_DURATION * 4:
            self._win.blit(
                self._1_txt,
                self._1_txt.get_rect(
                    center=(self._win_size_x // 2 - CELL_SIZE // 2,
                            self._win_size_y // 2)
                )
            )
        elif now - start_time >= READY_STEP_DURATION * 3:
            self._win.blit(
                self._2_txt,
                self._2_txt.get_rect(
                    center=(self._win_size_x // 2 - CELL_SIZE // 2,
                            self._win_size_y // 2)
                )
            )
        elif now - start_time >= READY_STEP_DURATION * 2:
            self._win.blit(
                self._3_txt,
                self._3_txt.get_rect(
                    center=(self._win_size_x // 2 - CELL_SIZE // 2,
                            self._win_size_y // 2)
                )
            )

    def _render_go(self) -> None:
        self._win.blit(
            self._go_txt,
            self._go_txt.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 2)
            )
        )

    def render_ready(self, start_time: float) -> None:
        self.__load_texts()
        now = time.perf_counter()
        if now - start_time <= READY_STEP_DURATION:
            self._render_ready()
        elif now - start_time <= READY_STEP_DURATION * 5:
            self._render_number(start_time, now)
        elif now - start_time <= READY_STEP_DURATION * 6:
            self._render_go()
