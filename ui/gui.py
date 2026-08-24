import pygame


class GUI:
    def __init__(self, title: str, size: tuple[int, int]) -> None:
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(size)

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()

    def quit(self) -> None:
        pygame.quit()
