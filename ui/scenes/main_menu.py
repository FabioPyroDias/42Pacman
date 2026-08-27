import pygame
from game import GameState
from consts import (COMMOM_TEXT_COLOR, GAME_TITLE_COLOR)


class MainMenu():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.title_font = pygame.font.SysFont(
            None,
            int(screen.get_height() * 0.15)
            )
        self.footer_font = pygame.font.SysFont(
            None,
            int(screen.get_height() * 0.028)
            )

    def render_menu(self, game_state: GameState) -> None:
        self._render_tile()
        self._render_cta(game_state.blink)

    def _render_tile(self) -> None:
        title = self.title_font.render(
            "PAC-MAN", 0, GAME_TITLE_COLOR
            )
        x, y = self.screen.get_size()
        self.screen.blit(title, title.get_rect(center=(x // 2, y // 6)))

    def _render_cta(self, blink: bool) -> None:
        x, y = self.screen.get_size()

        footer = self.footer_font.render(
            "H. Highscores  I. Instructions  ESC. Exit",
            0,
            COMMOM_TEXT_COLOR
            )
        self.screen.blit(footer, footer.get_rect(
            center=(x // 2, y - 20)))

        if blink:
            start_text = self.footer_font.render(
                        "press SPACE to start",
                        0,
                        COMMOM_TEXT_COLOR
                        )

            self.screen.blit(start_text, start_text.get_rect(
                    center=(x // 2, y // 2)))
