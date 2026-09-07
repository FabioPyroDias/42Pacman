import pygame
from .scenes import (
    MainMenu, Instructions, HUD, Gameplay, PauseMenu, HighscoreView,
    GameOver
    )
from game import GameState


Coordinates = tuple[int, int]


class GUI(Gameplay, HUD, MainMenu, Instructions, PauseMenu,
          HighscoreView, GameOver):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game_state: GameState, map_size: tuple[int, int]) -> None:
        super().__init__(win_size, title, game_state, map_size)

    def game(self) -> None:
        self.render_gameplay()
        self.render_hud()

    def menu(self) -> None:
        self.render_menu()

    def instructions(self) -> None:
        self.render_instructions()

    def pause(self) -> None:
        self.render_pause()

    def highscores(self) -> None:
        self.render_highscores()

    def game_over(self) -> None:
        self.render_game_over()

    def draw(self):
        draw_func = getattr(self, self._game_state.active_screen)
        assert draw_func is not None
        draw_func()
        self._win.blit(pygame.font.SysFont(None, 30).render(
            f"{round(self._game_state.clock.get_fps())}", 1, (255, 255, 255)),
                         (80, 80))  # debug
        pygame.display.update()

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()
