import pygame
import time
from typing import Literal
from maze import MazeAdapter
from consts import (
    PACMAN_DEATH_SPRITE_START_INDEX_Y, ENTITIES_UP_SPRITE_INDEX_Y,
    SCARED_TIME, SAFE_DEFAULTS
    )


class Entities:
    def __init__(self, pos: tuple[int, int], *,
                 sprite_x: int = 0, sprite_y: int = 0,
                 dead_sprite_x: int = 0, dead_sprite_y: int = 0,
                 direction: Literal['N', 'S', 'L', 'W'] = 'N') -> None:
        self.pos = pos
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.dead_sprite_x = dead_sprite_x
        self.dead_sprite_y = dead_sprite_y
        self.direction = direction
        self.alive = True
        self.last_frame_time = time.perf_counter()
        self.scared = False


class GameState:
    def __init__(self, active_screen: str, maze: MazeAdapter,
                 clock: pygame.time.Clock):
        self.active_screen = active_screen
        self.maze = maze
        self.in_game = False
        self.scared_time = SCARED_TIME
        self.clock = clock  # debug
        self.life = 3
        self.level = 1
        self.score = 100000000000000
        self.scared_start_time = 0.0
        self.flashing = False
        self.highscore_path = SAFE_DEFAULTS["highscore_filename"]

        self.player = Entities((0, 5), sprite_y=ENTITIES_UP_SPRITE_INDEX_Y,
                               dead_sprite_y=PACMAN_DEATH_SPRITE_START_INDEX_Y)
        self.pinky = Entities((0, 6), sprite_y=ENTITIES_UP_SPRITE_INDEX_Y)
        self.clyde = Entities((0, 7), sprite_y=ENTITIES_UP_SPRITE_INDEX_Y)
        self.inky = Entities((0, 8), sprite_y=ENTITIES_UP_SPRITE_INDEX_Y)
        self.blinky = Entities((0, 9), sprite_y=ENTITIES_UP_SPRITE_INDEX_Y)
