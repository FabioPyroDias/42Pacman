from ui import GUI
# from ui.gui import NGUI
from enums import Direction, GhostState
from maze import MazeAdapter
from game import GameState
import pygame
import random
import time

maze = MazeAdapter(size=(15, 15), seed=42)

running = True
state = GameState("menu", maze, pygame.time.Clock())
ngui = GUI((800, 600), "TEST", state, (len(maze.maze),
                                       len(maze.maze[0])))

frame_duration = 1 / 30  # fps alvo
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
                        state.player.direction = Direction.NORTH
                        state.inky.direction = Direction.NORTH
                        state.pinky.direction = Direction.NORTH
                        state.clyde.direction = Direction.NORTH
                        state.blinky.direction = Direction.NORTH
                    case pygame.K_LEFT:
                        state.player.direction = Direction.WEST
                        state.inky.direction = Direction.WEST
                        state.pinky.direction = Direction.WEST
                        state.clyde.direction = Direction.WEST
                        state.blinky.direction = Direction.WEST
                    case pygame.K_DOWN:
                        state.player.direction = Direction.SOUTH
                        state.inky.direction = Direction.SOUTH
                        state.pinky.direction = Direction.SOUTH
                        state.clyde.direction = Direction.SOUTH
                        state.blinky.direction = Direction.SOUTH
                    case pygame.K_RIGHT:
                        next_pos = state.player.get_next_position_on(state.player.pos, Direction.EAST)
                        while state.player.pos != next_pos:
                            state.player.set_next_direction(Direction.EAST)
                            state.player.update(0.006, state.maze)
                            ngui.draw()
                        state.inky.direction = Direction.EAST
                        state.pinky.direction = Direction.EAST
                        state.clyde.direction = Direction.EAST
                        state.blinky.direction = Direction.EAST

                    case pygame.K_d:
                        state.alive = not state.alive

                    case pygame.K_f:
                        state.blinky.state = GhostState.EATEN
                        state.pinky.state = GhostState.EATEN
                        state.inky.state = GhostState.EATEN
                        state.clyde.state = GhostState.EATEN

                    case pygame.K_s:
                        state.flashing = False
                        state.blinky.state = GhostState.FRIGHTENED
                        state.inky.state = GhostState.FRIGHTENED
                        state.pinky.state = GhostState.FRIGHTENED
                        state.clyde.state = GhostState.FRIGHTENED
                        state.scared_start_time = time.perf_counter()

                    case pygame.K_w:
                        state.blinky.state = GhostState.CHASE
                        state.inky.state = GhostState.CHASE
                        state.pinky.state = GhostState.CHASE
                        state.clyde.state = GhostState.CHASE

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
        state.blinky.state = GhostState.CHASE
        state.inky.state = GhostState.CHASE
        state.pinky.state = GhostState.CHASE
        state.clyde.state = GhostState.CHASE
        state.flashing = False
    elapsed = time.perf_counter() - current_time
pygame.quit()
