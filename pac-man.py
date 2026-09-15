from ui import GUI, handle_name_input
from highscore import Highscore
from enums import Direction, SceneState, GameState
from parser.parser import parser_configuration_file
from manager.game import Game
import pygame
import time
import os

# TODO
# adicionar "press enter to confirm"
# arrumar a validacao do nome

os.system("clear")
running = True
configs = parser_configuration_file("config.json")
highscores = Highscore("highscores.json")
game = Game(configs)
game.toggle_pause()
gui = GUI((800, 600), "PAC-MAN", game, game.maze,
          (game.maze.width, game.maze.height))

pause = False
last_time = time.perf_counter()
frame_duration = 1 / 60  # fps alvo
elapsed = 0  # usado para travar fps
player_name = ""
while running:
    if elapsed < frame_duration:  # para travar fps
        time.sleep(frame_duration - elapsed)
    now = time.perf_counter()
    delta = now - last_time
    last_time = now

    if (gui.active_scene != SceneState.READY
            or game.game_state in (GameState.RESPAWNING,
                                   GameState.RESTART_LEVEL)):
        game.update(delta)
        if pause and game.game_state == GameState.PLAYING:
            gui.active_scene = SceneState.READY
            game.toggle_pause()
            pause = False
    gui.update(game.frightened_timer, game.current_level_index,
               game.score, game.lives, game.game_state,
               player_name, highscores.scores, game.level_timer)
    for event in gui.get_event():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if gui.active_scene == SceneState.MENU:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_h:
                        gui.active_scene = SceneState.HIGHSCORES_VIEW
                    case pygame.K_i:
                        gui.active_scene = SceneState.INSTRUCTIONS
                    case pygame.K_SPACE:
                        gui.active_scene = SceneState.READY
                    case pygame.K_n:
                        gui.active_scene = SceneState.NAMEENTRY

            elif gui.active_scene in (SceneState.HIGHSCORES_VIEW,
                                      SceneState.INSTRUCTIONS):
                if event.key == pygame.K_ESCAPE:
                    gui.active_scene = SceneState.MENU

            elif gui.active_scene == SceneState.PAUSE:
                if event.key == pygame.K_ESCAPE:
                    gui.active_scene = SceneState.MENU
                    game.score = 0
                    game.setup_level()
                    game.toggle_pause()
                elif event.key == pygame.K_SPACE:
                    gui.active_scene = SceneState.GAMEPLAY
                    game.toggle_pause()

            elif gui.active_scene in (SceneState.GAME_OVER,
                                      SceneState.VICTORY):
                if event.key == pygame.K_DELETE:
                    gui.active_scene = SceneState.NAMEENTRY
                    print(gui.active_scene)

            elif gui.active_scene == SceneState.NAMEENTRY:
                if event.key == pygame.K_ESCAPE:
                    gui.active_scene = SceneState.MENU
                elif event.key == pygame.K_RETURN:
                    highscores.add_score(player_name, game.score)
                    gui.active_scene = SceneState.HIGHSCORES_VIEW
                else:
                    player_name = handle_name_input(
                        10,
                        player_name,
                        event
                        )

            elif game.game_state == GameState.RESPAWNING:
                continue

            elif gui.active_scene == SceneState.READY:
                continue

            elif gui.active_scene == SceneState.GAMEPLAY:
                match event.key:
                    case pygame.K_i:
                        game.cheat_toggle_invincible()
                    case pygame.K_l:
                        game.cheat_add_lives()
                    case pygame.K_SPACE:
                        gui.active_scene = SceneState.PAUSE
                        game.toggle_pause()
                    case pygame.K_w | pygame.K_UP:
                        game.set_player_direction(Direction.NORTH)
                    case pygame.K_d | pygame.K_RIGHT:
                        game.set_player_direction(Direction.EAST)
                    case pygame.K_s | pygame.K_DOWN:
                        game.set_player_direction(Direction.SOUTH)
                    case pygame.K_a | pygame.K_LEFT:
                        game.set_player_direction(Direction.WEST)
                    case pygame.K_v:
                        game.game_state = GameState.VICTORY

    if (game.game_state == GameState.GAME_OVER
            and gui.active_scene == SceneState.GAMEPLAY):
        gui.active_scene = SceneState.GAME_OVER
    elif (game.game_state == GameState.VICTORY
            and gui.active_scene == SceneState.GAMEPLAY):
        gui.active_scene = SceneState.VICTORY
    elif game.game_state in (GameState.RESTART_LEVEL,
                             GameState.RESPAWNING):
        pause = True
    elapsed = time.perf_counter() - now
pygame.quit()
