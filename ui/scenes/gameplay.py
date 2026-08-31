import pygame
from time import perf_counter
from consts import (
    CELL_SIZE, WALL_OFFSET, SPRITE_SIZE,
    PLAYER_SPRITE_LAST_INDEX_X, PLAYER_DOWN_SPRITE_INDEX_Y,
    PLAYER_LEFT_SPRITE_INDEX_Y, PLAYER_RIGTH_SPRITE_INDEX_Y,
    PLAYER_UP_SPRITE_INDEX_Y, PALYER_DEATH_SPRITE_LAST_INDEX_Y,
    PALYER_DEATH_SPRITE_START_INDEX_Y, GHOST_DOWN_SPRITE__INDEX_Y,
    GHOST_LEFT_SPRITE__INDEX_Y, GHOST_RIGHT_SPRITE__INDEX_Y,
    GHOST_SPRITE_LAST_INDEX_X, GHOST_UP_SPRITE__INDEX_Y
    )


class Gameplay:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.player_sprites = pygame.image.load("assets/pacman.xpm")
        self.blinky_sprites = pygame.image.load("assets/blinky.xpm")
        self.clyde_sprites = pygame.image.load("assets/clyde.xpm")
        self.inky_sprites = pygame.image.load("assets/inky.xpm")
        self.pinky_sprites = pygame.image.load("assets/pinky.xpm")

        self.player_sprite_move_x = 0
        self.ghost_sprite_move_x = 0
        self.player_sprite_death_x = 0

        self.player_death_index_y = PALYER_DEATH_SPRITE_START_INDEX_Y

        self.last_frame_time = perf_counter()
        self.frame_interval = 1 / 12

    def debug_sprites(self) -> None:
        self.screen.blit(self.player_sprites,
                         (0 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          PLAYER_UP_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )
        self.screen.blit(self.player_sprites,
                         (1 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          PLAYER_RIGTH_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )
        self.screen.blit(self.player_sprites,
                         (2 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          PLAYER_LEFT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )
        self.screen.blit(self.player_sprites,
                         (3 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          PLAYER_DOWN_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )
        self.screen.blit(self.player_sprites,
                         (4 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_death_x * SPRITE_SIZE,
                          self.player_death_index_y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.blinky_sprites,
                         (0 * CELL_SIZE,
                          1 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_DOWN_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.blinky_sprites,
                         (1 * CELL_SIZE,
                          1 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_UP_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.blinky_sprites,
                         (2 * CELL_SIZE,
                          1 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_LEFT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.blinky_sprites,
                         (3 * CELL_SIZE,
                          1 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_RIGHT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (0 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_DOWN_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (1 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_UP_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (2 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_LEFT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (3 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_RIGHT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (0 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_DOWN_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (1 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_UP_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (2 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_LEFT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (3 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_RIGHT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (0 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_DOWN_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (1 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_UP_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (2 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_LEFT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (3 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          GHOST_RIGHT_SPRITE__INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

    def debug_animate(self) -> None:
        self.debug_sprites()
        now = perf_counter()
        if not (now - self.last_frame_time >= self.frame_interval):
            return
        self.last_frame_time = now

        if self.player_sprite_death_x == PLAYER_SPRITE_LAST_INDEX_X:
            self.player_sprite_death_x = 0
            if self.player_death_index_y == PALYER_DEATH_SPRITE_LAST_INDEX_Y:
                self.player_death_index_y = PALYER_DEATH_SPRITE_START_INDEX_Y
            else:
                self.player_death_index_y += 1
        else:
            self.player_sprite_death_x += 1

        if self.player_sprite_move_x == PLAYER_SPRITE_LAST_INDEX_X:
            self.player_sprite_move_x = 0
        else:
            self.player_sprite_move_x += 1

        if self.ghost_sprite_move_x == GHOST_SPRITE_LAST_INDEX_X:
            self.ghost_sprite_move_x = 0
        else:
            self.ghost_sprite_move_x += 1
