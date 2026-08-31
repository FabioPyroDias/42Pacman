import pygame
from time import perf_counter
from game import GameState, Entities
from consts import (
    CELL_SIZE, WALL_OFFSET, SPRITE_SIZE,
    PLAYER_SPRITE_LAST_INDEX_X, PALYER_DEATH_SPRITE_LAST_INDEX_Y,
    PALYER_DEATH_SPRITE_START_INDEX_Y, GHOST_SPRITE_LAST_INDEX_X,
    ENTITIES_DOWN_SPRITE_INDEX_Y, ENTITIES_LEFT_SPRITE_INDEX_Y,
    ENTITIES_RIGHT_SPRITE_INDEX_Y, ENTITIES_UP_SPRITE_INDEX_Y
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

    def draw_entities(self, game_state: GameState) -> None:
        if not game_state.player_alive:
            self.animate_entite_death(self.player_sprites, game_state.player,
                                      PLAYER_SPRITE_LAST_INDEX_X,
                                      PALYER_DEATH_SPRITE_LAST_INDEX_Y,
                                      PALYER_DEATH_SPRITE_START_INDEX_Y)
            self.animate_entitie(self.blinky_sprites, game_state.blinky,
                                 GHOST_SPRITE_LAST_INDEX_X)
            self.animate_entitie(self.inky_sprites, game_state.inky,
                                 GHOST_SPRITE_LAST_INDEX_X)
            self.animate_entitie(self.clyde_sprites, game_state.clyde,
                                 GHOST_SPRITE_LAST_INDEX_X)
            self.animate_entitie(self.pinky_sprites, game_state.pinky,
                                 GHOST_SPRITE_LAST_INDEX_X)
        else:
            self.animate_entitie(self.player_sprites, game_state.player,
                                 PLAYER_SPRITE_LAST_INDEX_X)
            self.animate_entitie(self.blinky_sprites, game_state.blinky,
                                 GHOST_SPRITE_LAST_INDEX_X)
            self.animate_entitie(self.inky_sprites, game_state.inky,
                                 GHOST_SPRITE_LAST_INDEX_X)
            self.animate_entitie(self.clyde_sprites, game_state.clyde,
                                 GHOST_SPRITE_LAST_INDEX_X)
            self.animate_entitie(self.pinky_sprites, game_state.pinky,
                                 GHOST_SPRITE_LAST_INDEX_X)

    def draw_sprite(self, sprite: pygame.Surface,
                    pos: tuple[int, int]) -> None:
        self.screen.blit(sprite, pos)

    def animate_entitie(self, sprite: pygame.Surface,
                        entitie: Entities, last_index_x: int) -> None:
        match entitie.direction:
            case 'N':
                entitie.sprite_y = ENTITIES_UP_SPRITE_INDEX_Y
            case 'L':
                entitie.sprite_y = ENTITIES_RIGHT_SPRITE_INDEX_Y
            case 'W':
                entitie.sprite_y = ENTITIES_LEFT_SPRITE_INDEX_Y
            case 'S':
                entitie.sprite_y = ENTITIES_DOWN_SPRITE_INDEX_Y

        self.draw_sprite(sprite.subsurface(
            (entitie.sprite_x * SPRITE_SIZE,
             entitie.sprite_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)),
             (entitie.pos[0] * CELL_SIZE + WALL_OFFSET,
              entitie.pos[1] * CELL_SIZE + WALL_OFFSET)
             )
        now = perf_counter()
        if not (now - entitie.last_frame_time >= self.frame_interval):
            return
        entitie.last_frame_time = now
        if entitie.sprite_x == last_index_x:
            entitie.sprite_x = 0
        else:
            entitie.sprite_x += 1

    def animate_entite_death(self, sprite: pygame.Surface,
                             entitie: Entities,
                             last_index_x: int,
                             last_index_y: int,
                             start_index_y: int) -> None:
        self.draw_sprite(sprite.subsurface(
            (entitie.dead_sprite_x * SPRITE_SIZE,
             entitie.dead_sprite_y * SPRITE_SIZE,
             SPRITE_SIZE, SPRITE_SIZE)),
             (entitie.pos[0] * CELL_SIZE + WALL_OFFSET,
              entitie.pos[1] * CELL_SIZE + WALL_OFFSET)
             )
        now = perf_counter()
        if not (now - entitie.last_frame_time >= self.frame_interval):
            return
        entitie.last_frame_time = now
        if entitie.dead_sprite_x == last_index_x:
            entitie.dead_sprite_x = 0
            if entitie.dead_sprite_y == last_index_y:
                entitie.dead_sprite_y = start_index_y
            else:
                entitie.dead_sprite_y += 1
        else:
            entitie.dead_sprite_x += 1

    def debug_sprites(self) -> None:
        self.screen.blit(self.player_sprites,
                         (0 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_UP_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )
        self.screen.blit(self.player_sprites,
                         (1 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )
        self.screen.blit(self.player_sprites,
                         (2 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_LEFT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )
        self.screen.blit(self.player_sprites,
                         (3 * CELL_SIZE + WALL_OFFSET,
                          0 * CELL_SIZE + WALL_OFFSET),
                         (self.player_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_DOWN_SPRITE_INDEX_Y * SPRITE_SIZE,
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
                          ENTITIES_DOWN_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.blinky_sprites,
                         (1 * CELL_SIZE,
                          1 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_UP_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.blinky_sprites,
                         (2 * CELL_SIZE,
                          1 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_LEFT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.blinky_sprites,
                         (3 * CELL_SIZE,
                          1 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (0 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (1 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (2 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.clyde_sprites,
                         (3 * CELL_SIZE,
                          2 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (0 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (1 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (2 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.inky_sprites,
                         (3 * CELL_SIZE,
                          3 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (0 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (1 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (2 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
                          SPRITE_SIZE, SPRITE_SIZE)
                         )

        self.screen.blit(self.pinky_sprites,
                         (3 * CELL_SIZE,
                          4 * CELL_SIZE),
                         (self.ghost_sprite_move_x * SPRITE_SIZE,
                          ENTITIES_RIGHT_SPRITE_INDEX_Y * SPRITE_SIZE,
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
