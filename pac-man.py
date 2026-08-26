from ui import GUI
from maze import MazeAdapter
from game import GameState
import pygame
import random

maze = MazeAdapter(seed=42)
for line in maze.maze:
    print(line)
gui = GUI("TEST", (len(maze.maze) * 50, len(maze.maze[0]) * 50))
running = True
state = GameState("menu", maze)


while running:
    gui.draw(game_state=state)
    for event in gui.get_event():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and state.in_game:
                maze.regenerate(random.randint(-100000, 100000))
                print("R")
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
gui.quit()
