import pygame


class Menu():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def render_menu(self, hi)

    def _render_tile(self) -> None:
        self.screen.fill((0, 0, 30))
        title = pygame.font.SysFont(None, size=78).render("PAC-MAN", 0, (230, 230, 50))
        x, y = self.screen.get_size()
        self.screen.blit(title, title.get_rect(center=(x // 2, y // 6)))
        pygame.display.update()
