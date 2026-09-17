"""Pac-Man application entry point."""

import sys
import time
import pygame
from gui import GUI
from manager import Game
from highscore import Highscore
from enums import GameState, SceneState, Direction
from parser import parser_configuration_file
from consts import (
    MENU_WIN_SIZE, FRAME_DURATION
)


def main() -> None:
    """
    Main entry point for the PAC-MAN game.

    This function initializes the game configuration, sets up the game loop,
    and handles user input for controlling the game. It manages the game state,
    updates the GUI, and processes events such as key presses and quitting the
    game.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Notes:
        - The game can be paused and resumed.
        - The function handles different scenes including the menu, gameplay,
        high scores, and instructions.
        - Player input is processed for movement and menu navigation.
        - The game state is updated based on player actions and game events.
    """
    config_path = ""
    if len(sys.argv) >= 2:
        config_path = sys.argv[1]
    config = parser_configuration_file(config_path)
    highscore = Highscore(config["highscore_filename"])
    game = Game(config)
    game.toggle_pause()
    gui = GUI(MENU_WIN_SIZE, "PAC-MAN", game, game.maze)

    running = True
    in_countdown = False

    player_name = ""

    delta = 0.0
    frame_time = 0.0
    last_frame_time = time.perf_counter()

    while running:
        if frame_time < FRAME_DURATION:
            time.sleep(FRAME_DURATION - frame_time)
        now = time.perf_counter()
        delta = now - last_frame_time
        last_frame_time = now

        if gui.active_scene != SceneState.READY:
            game.update(delta)
            if in_countdown and game.game_state == GameState.PLAYING:
                game.toggle_pause()
                gui.active_scene = SceneState.READY
                in_countdown = False

        if gui.maze != game.maze:
            game.toggle_pause()
            gui.active_scene = SceneState.READY

        gui.update(game.frightened_timer, game.current_level_index,
                   game.score, game.lives, game.game_state,
                   player_name, highscore.scores, game.level_timer,
                   game.maze)

        for event in gui.get_event():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if gui.active_scene == SceneState.MENU:
                    match event.key:
                        case pygame.K_SPACE:
                            gui.active_scene = SceneState.READY
                            game.reset_game()
                        case pygame.K_ESCAPE:
                            running = False
                        case pygame.K_h:
                            gui.active_scene = SceneState.HIGHSCORES_VIEW
                        case pygame.K_i:
                            gui.active_scene = SceneState.INSTRUCTIONS

                elif gui.active_scene in (SceneState.HIGHSCORES_VIEW,
                                          SceneState.INSTRUCTIONS):
                    match event.key:
                        case pygame.K_ESCAPE:
                            gui.active_scene = SceneState.MENU

                elif gui.active_scene == SceneState.GAMEPLAY:
                    match event.key:
                        case pygame.K_w | pygame.K_UP:
                            game.set_player_direction(Direction.NORTH)
                        case pygame.K_d | pygame.K_RIGHT:
                            game.set_player_direction(Direction.EAST)
                        case pygame.K_s | pygame.K_DOWN:
                            game.set_player_direction(Direction.SOUTH)
                        case pygame.K_a | pygame.K_LEFT:
                            game.set_player_direction(Direction.WEST)
                        case pygame.K_SPACE:
                            game.toggle_pause()
                            gui.active_scene = SceneState.PAUSE

                elif gui.active_scene == SceneState.PAUSE:
                    match event.key:
                        case pygame.K_SPACE:
                            game.toggle_pause()
                            gui.active_scene = SceneState.GAMEPLAY
                        case pygame.K_ESCAPE:
                            gui.active_scene = SceneState.MENU

                elif gui.active_scene == SceneState.NAME_ENTRY:
                    match event.key:
                        case pygame.K_ESCAPE:
                            gui.active_scene = SceneState.MENU
                            player_name = ""
                        case pygame.K_RETURN:
                            gui.invalid_player_name = (
                                not highscore.validate_name(player_name)
                                )
                            if not gui.invalid_player_name:
                                highscore.add_score(player_name, game.score)
                                gui.active_scene = SceneState.HIGHSCORES_VIEW
                                player_name = ""
                        case _:
                            if not gui.invalid_player_name:
                                player_name = gui.handle_name_input(
                                    10,
                                    player_name,
                                    event
                                )

        if (game.game_state == GameState.GAME_OVER
                and gui.active_scene == SceneState.GAMEPLAY):
            gui.active_scene = SceneState.GAME_OVER
        elif (game.game_state == GameState.VICTORY
                and gui.active_scene == SceneState.GAMEPLAY):
            gui.active_scene = SceneState.VICTORY
        elif game.game_state in (GameState.RESPAWNING,
                                 GameState.RESTART_LEVEL):
            in_countdown = True
        frame_time = time.perf_counter() - last_frame_time

    pygame.quit()


main()
