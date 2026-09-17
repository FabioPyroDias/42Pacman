"""GUI coordinator for scene rendering and input flow."""

import pygame
import time
from manager.game import Game
from enums import GameState, SceneState
from maze.maze_adapter import MazeAdapter
from .scenes import (
    MainMenu, Instructions, HUD, Gameplay, PauseMenu, HighscoreView,
    GameOver, Victory, NameEntry, Ready
    )
from consts import (
    READY_TOTAL_DURATION, RESULT_SCREEN_TEXT_DURATION,
    )


class GUI(Gameplay, HUD, MainMenu, Instructions,
          HighscoreView, PauseMenu, GameOver, Victory,
          NameEntry, Ready):
    def __init__(self, win_size: tuple[int, int], title: str,
                 game: Game, maze: MazeAdapter) -> None:
        super().__init__(win_size, title, game, maze)
        self.active_scene = SceneState.MENU
        self.invalid_player_name = False
        self.__ready = True
        self.__start_time = 0.0

    def update(self, frightened_timer: float, level: int,
               score: int, lives: int, game_state: GameState,
               player_name: str, highscore: list[dict[str, str | int]],
               timer: float, maze: MazeAdapter) -> None:

        if (not self.__ready
                and game_state not in (GameState.GAME_OVER,
                                       GameState.VICTORY)):
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
                self.render_gameplay(frightened_timer, game_state, maze)
                self.render_hud(level, score, lives, timer, game_state)

            case SceneState.READY:
                self.render_gameplay(frightened_timer, game_state, maze,
                                     True)
                self.render_hud(level, score, lives, timer, game_state)
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
                    self.active_scene = SceneState.NAME_ENTRY
                    self.__start_time = 0.0
                self.render_game_over()

            case SceneState.VICTORY:
                if self.__start_time == 0.0:
                    self.__start_time = time.perf_counter()
                delta = time.perf_counter() - self.__start_time
                if delta >= RESULT_SCREEN_TEXT_DURATION:
                    self.active_scene = SceneState.NAME_ENTRY
                    self.__start_time = 0.0
                self.render_victory()

            case SceneState.NAME_ENTRY:
                if self.invalid_player_name:
                    if self.__start_time == 0.0:
                        self.__start_time = time.perf_counter()
                    if time.perf_counter() - self.__start_time >= 1:
                        self.invalid_player_name = False
                        self.__start_time = 0.0
                self.render_name_entry(player_name, self.invalid_player_name)

        pygame.display.update()

    def get_event(self) -> list[pygame.event.Event]:
        return pygame.event.get()
