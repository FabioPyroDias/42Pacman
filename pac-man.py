from ui import GUI
from maze import MazeAdapter
from game import GameState
from consts import CELL_SIZE
import pygame
import random
import time

maze = MazeAdapter(seed=42)
for line in maze.maze:
    print(line)
gui = GUI("TEST", (len(maze.maze) * CELL_SIZE,
                   len(maze.maze[0]) * CELL_SIZE))
running = True
state = GameState("menu", maze, pygame.time.Clock())

frame_duration = 1 / 60  # fps alvo
elapsed = 0  # usado para travar fps
last_blink = time.perf_counter()
while running:
    if elapsed < frame_duration:  # para travar fps
        time.sleep(frame_duration - elapsed)
    state.clock.tick()  # debug (tirar depois)
    current_time = time.perf_counter()
    if not state.in_game and current_time - last_blink >= 0.5:
        last_blink = current_time
        state.blink = not state.blink
    gui.draw(game_state=state)
    for event in gui.get_event():
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
                        state.player_alive = not state.player_alive

                    case pygame.K_ESCAPE:
                        state.active_screen = "menu"
                        state.in_game = False
                        print("ESC")
                    case pygame.K_r:
                        maze.regenerate(random.randint(-100000, 100000))
                        print("R")

            else:
                match event.key:
                    case pygame.K_SPACE:
                        state.active_screen = "game"
                        state.in_game = True
                        print("GAME")
                    case pygame.K_i:
                        state.active_screen = "instructions"
                    case pygame.K_ESCAPE:
                        running = False
                        print("ESC")

    elapsed = time.perf_counter() - current_time
gui.quit()
