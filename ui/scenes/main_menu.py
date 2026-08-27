import pygame
from game import GameState


class MainMenu():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def render_menu(self, game_state: GameState,
                    highscore_filename: str = "",) -> None:
        self.screen.fill((0, 0, 30))
        self._render_tile()
        self._render_cta(game_state.blink)

    def _render_tile(self) -> None:
        title = pygame.font.SysFont(None, size=78).render(
            "PAC-MAN", 0, (230, 230, 50)
            )
        x, y = self.screen.get_size()
        self.screen.blit(title, title.get_rect(center=(x // 2, y // 6)))

    def _render_cta(self, blink: bool) -> None:
        font = pygame.font.SysFont(None, size=20)
        x, y = self.screen.get_size()

        footer = font.render(
            "H. Highscores  I. Instructions  ESC. Exit",
            0,
            (255, 255, 255)
            )
        self.screen.blit(footer, footer.get_rect(
            center=(x // 2, y - 20)))

        if blink:
            start_text = font.render(
                        "press SPACE to start",
                        0,
                        (255, 255, 255)
                        )

            self.screen.blit(start_text, start_text.get_rect(
                    center=(x // 2, y // 2)))
