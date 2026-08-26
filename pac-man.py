from ui import GUI
from maze import MazeAdapter
import pygame
import random

maze = MazeAdapter(seed=42)
for line in maze.maze:
    print(line)
gui = GUI("TEST", (len(maze.maze) * 50, len(maze.maze[0]) * 50))
running = True

while running:
    #gui.draw_maze(maze)
    gui.draw_menu()
    for event in gui.get_event():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            maze.regenerate(random.randint(-100000, 100000))
gui.quit()
