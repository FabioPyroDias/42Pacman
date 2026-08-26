import pygame


class MainMenu():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def render_menu(self, highscore_filename: str = "") -> None:
        self.screen.fill((0, 0, 30))
        self._render_tile()
        self._render_cta()

    def _render_tile(self) -> None:
        title = pygame.font.SysFont(None, size=78).render(
            "PAC-MAN", 0, (230, 230, 50)
            )
        x, y = self.screen.get_size()
        self.screen.blit(title, title.get_rect(center=(x // 2, y // 6)))

    def _render_cta(self) -> None:
        font = pygame.font.SysFont(None, size=20)
        start_text = font.render(
            "press SPACE to start",
            0,
            (255, 255, 255)
            )
        footer = font.render(
            "H. Highscores  C. Instructions  ESC. Exit",
            0,
            (255, 255, 255)
            )

        x, y = self.screen.get_size()

        self.screen.blit(start_text, start_text.get_rect(
                center=(x // 2, y // 2)))
        self.screen.blit(footer, footer.get_rect(
                    center=(x // 2, y - 20)))
