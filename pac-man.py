from ui import GUI
# from ui.gui import NGUI
from maze import MazeAdapter
from game import GameState
import pygame
import random
import time

maze = MazeAdapter(size=(15, 15), seed=42)
for line in maze.maze:
    print(line)


running = True
state = GameState("menu", maze, pygame.time.Clock())
ngui = GUI((800, 600), "TEST", state, (len(maze.maze),
                                       len(maze.maze[0])))

frame_duration = 1 / 60  # fps alvo
elapsed = 0  # usado para travar fps
last_blink = time.perf_counter()
while running:
    if elapsed < frame_duration:  # para travar fps
        time.sleep(frame_duration - elapsed)
    state.clock.tick()  # debug (tirar depois)
    current_time = time.perf_counter()

    ngui.draw()
    for event in ngui.get_event():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if state.in_game:
                match event.key:
                    case pygame.K_UP:
                        state.player.direction = 'N'
                        state.inky.direction = 'N'
                        state.pinky.direction = 'N'
                        state.clyde.direction = 'N'
                        state.blinky.direction = 'N'
                    case pygame.K_LEFT:
                        state.player.direction = 'W'
                        state.inky.direction = 'W'
                        state.pinky.direction = 'W'
                        state.clyde.direction = 'W'
                        state.blinky.direction = 'W'
                    case pygame.K_DOWN:
                        state.player.direction = 'S'
                        state.inky.direction = 'S'
                        state.pinky.direction = 'S'
                        state.clyde.direction = 'S'
                        state.blinky.direction = 'S'
                    case pygame.K_RIGHT:
                        state.player.direction = 'L'
                        state.inky.direction = 'L'
                        state.pinky.direction = 'L'
                        state.clyde.direction = 'L'
                        state.blinky.direction = 'L'

                    case pygame.K_d:
                        state.player.alive = not state.player.alive

                    case pygame.K_f:
                        state.blinky.alive = not state.blinky.alive
                        state.pinky.alive = not state.pinky.alive
                        state.inky.alive = not state.inky.alive
                        state.clyde.alive = not state.clyde.alive

                    case pygame.K_s:
                        state.flashing = False
                        state.blinky.scared = True
                        state.inky.scared = True
                        state.pinky.scared = True
                        state.clyde.scared = True
                        state.scared_start_time = time.perf_counter()

                    case pygame.K_g:
                        if state.active_screen != "game_over":
                            state.active_screen = "game_over"
                        else:
                            state.active_screen = "game"

                    case pygame.K_ESCAPE:
                        state.active_screen = "menu"
                        state.in_game = False
                        print("ESC")
                    case pygame.K_r:
                        maze.regenerate(random.randint(-100000, 100000))
                        print("R")

                    case pygame.K_SPACE:
                        state.active_screen = "pause" if state.active_screen != "pause" else "game"

            else:
                match event.key:
                    case pygame.K_SPACE:
                        state.active_screen = "game"
                        state.in_game = True
                        print("GAME")
                    case pygame.K_i:
                        state.active_screen = "instructions"
                    case pygame.K_h:
                        state.active_screen = "highscores"
                    case pygame.K_ESCAPE:
                        if state.active_screen != "menu":
                            state.active_screen = "menu"
                        else:
                            running = False
                        print("ESC")
    if current_time - state.scared_start_time >= state.scared_time:
        state.blinky.scared = False
        state.inky.scared = False
        state.pinky.scared = False
        state.clyde.scared = False
        state.flashing = False
    elapsed = time.perf_counter() - current_time
pygame.quit()
