import pygame
from time import perf_counter
from consts import CELL_SIZE, WALL_OFFSET, SPRITE_SIZE


class Gameplay:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.player_up = pygame.image.load("assets/pacman_up.xpm")
        self.player_down = pygame.image.load("assets/pacman_down.xpm")
        self.player_left = pygame.image.load("assets/pacman_left.xpm")
        self.player_right = pygame.image.load("assets/pacman_right.xpm")
        self.player_death = pygame.image.load("assets/pacman_death.xpm")

        self.player_sprite_x_move_limit = 3
        self.player_sprite_x_death_limit = 7
        self.player_sprite_y_death_limit = 1

        self.player_sprite_move_x = 0
        self.player_sprite_death_x = 0
        self.player_sprite_death_y = 0

        self.last_frame_time = perf_counter()
        self.frame_interval = 1 / 12

    def debug_sprites(self) -> None:
        self.screen.blit(self.player_up,
                         (0 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          0,
                          40, 40)
                         )
        self.screen.blit(self.player_down,
                         (1 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          0,
                          40, 40)
                         )
        self.screen.blit(self.player_right,
                         (2 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          0,
                          40, 40)
                         )
        self.screen.blit(self.player_left,
                         (3 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          0,
                          40, 40)
                         )
        self.screen.blit(self.player_death,
                         (4 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_death_x * SPRITE_SIZE,
                          self.player_sprite_death_y * SPRITE_SIZE,
                          40, 40)
                         )

    def debug_animate(self) -> None:
        self.debug_sprites()
        now = perf_counter()
        if not (now - self.last_frame_time >= self.frame_interval):
            return
        self.last_frame_time = now

        if self.player_sprite_death_x == self.player_sprite_x_death_limit:
            self.player_sprite_death_x = 0
            if self.player_sprite_death_y == self.player_sprite_y_death_limit:
                self.player_sprite_death_y = 0
            else:
                self.player_sprite_death_y += 1
        else:
            self.player_sprite_death_x += 1

        if self.player_sprite_move_x == self.player_sprite_x_move_limit:
            self.player_sprite_move_x = 0
        else:
            self.player_sprite_move_x += 1
