from ui import GUI
from enums import Direction, SceneState, GameState
from parser.parser import parser_configuration_file
from manager.game import Game
import pygame
import time

running = True
configs = parser_configuration_file("configs.json")
game = Game(configs)
game.toggle_pause()
gui = GUI((800, 600), "PAC-MAN", game, game.maze,
          (game.maze.width, game.maze.height),
          {"p1": 100})
clock = pygame.time.Clock()

active_scene = SceneState.MENU

last_time = time.perf_counter()
frame_duration = 1 / 60  # fps alvo
elapsed = 0  # usado para travar fps
while running:
    if elapsed < frame_duration:  # para travar fps
        time.sleep(frame_duration - elapsed)
    now = time.perf_counter()
    delta = now - last_time
    last_time = now
    clock.tick()  # debug (tirar depois)

    game.update(delta)  # 0.028
    gui.update(active_scene, game.frightened_timer, game.current_level_index,
               game.score, game.lives, game.game_state, clock)
    for event in gui.get_event():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if active_scene == SceneState.MENU:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_h:
                        active_scene = SceneState.HIGHSCORES_VIEW
                    case pygame.K_i:
                        active_scene = SceneState.INSTRUCTIONS
                    case pygame.K_SPACE:
                        active_scene = SceneState.GAMEPLAY
                        game.toggle_pause()
            elif active_scene in (SceneState.HIGHSCORES_VIEW,
                                  SceneState.INSTRUCTIONS):
                if event.key == pygame.K_ESCAPE:
                    active_scene = SceneState.MENU
            elif active_scene == SceneState.PAUSE:
                if event.key == pygame.K_ESCAPE:
                    active_scene = SceneState.MENU
                    game.setup_level()
                    game.toggle_pause()
            else:
                match event.key:
                    case pygame.K_SPACE:
                        active_scene = (
                            SceneState.PAUSE
                            if active_scene == SceneState.GAMEPLAY
                            else SceneState.GAMEPLAY
                            )
                        game.toggle_pause()
                    case pygame.K_w | pygame.K_UP:
                        game.set_player_direction(Direction.NORTH)
                    case pygame.K_d | pygame.K_RIGHT:
                        game.set_player_direction(Direction.EAST)
                    case pygame.K_s | pygame.K_DOWN:
                        game.set_player_direction(Direction.SOUTH)
                    case pygame.K_a | pygame.K_LEFT:
                        game.set_player_direction(Direction.WEST)
    if game.game_state == GameState.GAME_OVER:
        active_scene = SceneState.GAMEOVER
    elif game.game_state == GameState.VICTORY:
        active_scene = SceneState.VICTORY
    elapsed = time.perf_counter() - now
pygame.quit()
