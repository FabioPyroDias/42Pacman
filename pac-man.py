from ui import GUI
from maze import MazeAdapter
from game import GameState
from consts import CELL_SIZE, WALL_THICKNESS
import pygame
import random
import time

maze = MazeAdapter(seed=42)
for line in maze.maze:
    print(line)
gui = GUI("TEST", (len(maze.maze) * CELL_SIZE + WALL_THICKNESS,
                   len(maze.maze[0]) * CELL_SIZE + WALL_THICKNESS))
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

            if event.key == pygame.K_r and state.in_game:
                maze.regenerate(random.randint(-100000, 100000))
                print("R")

            if event.key == pygame.K_i and not state.in_game:
                state.active_screen = "instructions"

            if event.key == pygame.K_ESCAPE:
                if state.in_game:
                    state.active_screen = "menu"
                    state.in_game = False
                else:
                    running = False
                print("ESC")

            if event.key == pygame.K_SPACE:
                state.active_screen = "game"
                state.in_game = True
                print("GAME")
    elapsed = time.perf_counter() - current_time
gui.quit()
