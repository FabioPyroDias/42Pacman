import pygame
from .base_render import BaseRender
from game.game_state import GameState
from consts import (
    COMMOM_TEXT_COLOR, BACKGROUND_COLOR, INSTRUCTIONS_LIST,
    EXPECTECTED_INSTRUCTIONS_LEN
    )


INSTRUCTIONS = [first + "."*abs(
    len(first + second) + 2 - EXPECTECTED_INSTRUCTIONS_LEN
    ) + second
    for first, second in INSTRUCTIONS_LIST]


class Instructions(BaseRender):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game_state: GameState) -> None:
        super().__init__(win_size, title, game_state)
        self.__updated = False
        self.__fonts_loaded = False
        self.__text_loaded = False

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
        self._instructions_font = pygame.font.SysFont(
                    None,
                    int(self._win_size_y * 0.05)
                    )

        self._intructions_heigth = self._instructions_font.get_linesize()
        self.__fonts_loaded = True

    def __load_text(self) -> None:
        self.__load_fonts()
        if hasattr(self, "_subtitle"):
            self.__text_loaded = False
        if self.__text_loaded:
            return

        self._subtitle = self._subtitle_font.render(
                "INSTRUCTIONS",
                0,
                COMMOM_TEXT_COLOR
                )

        self._instructions_list = [
            self._instructions_font.render(
                instructions_text,
                0,
                COMMOM_TEXT_COLOR
                ) for instructions_text in INSTRUCTIONS
        ]

        self.__text_loaded = True

    def _render_instructions_subtitle(self) -> None:
        self._win.blit(
            self._subtitle,
            self._subtitle.get_rect(
                center=(self._win_size_x // 2,
                        self._win_size_y // 6)
                ))

    def _render_commands(self) -> None:
        for i, instruction_txt in enumerate(self._instructions_list, 1):
            self._win.blit(
                instruction_txt,
                instruction_txt.get_rect(
                    center=(self._win_size_x // 2,
                            self._win_size_y // 3 +
                            (self._intructions_heigth + 10) * i
                            )
                    )
            )

    def render_instructions(self) -> None:
        self.__update()
        self.__load_text()
        self._win.blit(
            self._background,
            (0, 0)
        )
        self._render_instructions_subtitle()
        self._render_commands()
