import pygame
import time
from manager.game import Game
from enums import GameState, SceneState
from maze.maze_adapter import MazeAdapter
from .scenes import (
    MainMenu, Instructions, HUD, Gameplay, PauseMenu, HighscoreView,
    GameOver, Victory, NameEntry, Ready
    )
from consts import READY_TOTAL_DURATION, RESULT_SCREEN_TEXT_DURATION


class GUI(Gameplay, HUD, MainMenu, Instructions,
          HighscoreView, PauseMenu, GameOver, Victory,
          NameEntry, Ready):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter,
                 map_size: tuple[int, int]) -> None:
        super().__init__(win_size, title, game, maze, map_size=map_size)
        self.active_scene = SceneState.MENU
        self.__ready = True
        self.__start_time = 0.0

    def update(self, frightened_timer: float, level: int,
               score: int, lives: int, game_state: GameState,
               player_name: str, highscore: list[dict[str, str | int]],
               timer: float) -> None:
        if not self.__ready and game_state not in (GameState.GAME_OVER,
                                                   GameState.VICTORY):
            self.active_scene = SceneState.GAMEPLAY
            self.__ready = True
            self._game.toggle_pause()
        match self.active_scene:
            case SceneState.MENU:
                self.render_menu()
            case SceneState.INSTRUCTIONS:
                self.render_instructions()
            case SceneState.HIGHSCORES_VIEW:
                self.render_highscores(highscore)
            case SceneState.GAMEPLAY:
                self.render_gameplay(frightened_timer, game_state)
                self.render_hud(level, score, lives, timer)
            case SceneState.READY:
                self.render_gameplay(frightened_timer, game_state,
                                     True)
                self.render_hud(level, score, lives, timer)
                if self.__start_time == 0.0:
                    self.__start_time = time.perf_counter()
                self.render_ready(self.__start_time)
                delta = time.perf_counter() - self.__start_time
                if delta >= READY_TOTAL_DURATION:
                    self.__start_time = 0.0
                    self.__ready = False
                    self.active_scene = SceneState.GAMEPLAY
            case SceneState.PAUSE:
                self.render_pause()
            case SceneState.GAME_OVER:
                if self.__start_time == 0.0:
                    self.__start_time = time.perf_counter()
                delta = time.perf_counter() - self.__start_time
                if delta >= RESULT_SCREEN_TEXT_DURATION:
                    self.active_scene = SceneState.NAMEENTRY
                    self.__start_time = 0.0
                self.render_game_over()
            case SceneState.VICTORY:
                if self.__start_time == 0.0:
                    self.__start_time = time.perf_counter()
                delta = time.perf_counter() - self.__start_time
                if delta >= RESULT_SCREEN_TEXT_DURATION:
                    self.active_scene = SceneState.NAMEENTRY
                    self.__start_time = 0.0
                self.render_victory()
            case SceneState.NAMEENTRY:
                self.render_name_entry(player_name)
            case _:
                raise Exception(f"{self.active_scene} not implemented")
        pygame.display.update()

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()
