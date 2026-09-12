import pygame
from manager.game import Game
from enums import GameState, SceneState
from maze.maze_adapter import MazeAdapter
from .scenes import (
    MainMenu, Instructions, HUD, Gameplay, PauseMenu, HighscoreView,
    GameOver, Victory
    )


Coordinates = tuple[int, int]


class GUI(Gameplay, HUD, MainMenu, Instructions,
          HighscoreView, PauseMenu, GameOver, Victory):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter, map_size: tuple[int, int],
                 highscores: dict[str, int]) -> None:
        super().__init__(win_size, title, game, maze, map_size, highscores)

    def update(self, active_scene: SceneState, frightened_timer: float,
               level: int, score: int, lives: int, game_state: GameState,
               clock: pygame.time.Clock) -> None:
        match active_scene:
            case SceneState.MENU:
                self.render_menu()
            case SceneState.INSTRUCTIONS:
                self.render_instructions()
            case SceneState.HIGHSCORES_VIEW:
                self.render_highscores()
            case SceneState.GAMEPLAY:
                self.render_gameplay(frightened_timer, game_state)
                self.render_hud(level, score, lives)
            case SceneState.PAUSE:
                self.render_pause()
            case SceneState.GAMEOVER:
                self.render_game_over()
            case SceneState.VICTORY:
                self.render_victory()
            case _:
                raise Exception(f"{active_scene} not implemented")
        self._win.blit(pygame.font.SysFont(None, 30).render(
            f"{round(clock.get_fps())}", 1, (255, 255, 255)),
                         (80, 80))  # debug
        pygame.display.update()

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()
