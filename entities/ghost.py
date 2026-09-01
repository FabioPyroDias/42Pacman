from maze.maze_adapter import MazeAdapter
from entities.entity import MovableEntity
from enums import Direction, GhostState
from random import randint


class Ghost(MovableEntity):
    """Represents a ghost entity in the maze.

    Attributes:
        state (GhostState): The current behavioral state of the ghost.
        scatter_area_top_left (tuple[int, int]): Top left corner of the
            ghost's scatter zone.
        scatter_area_bottom_right (tuple[int, int]): Bottom right corner of the
            ghost's scatter zone.
        scatter_target (tuple[int, int]): Current destination within the
            scatter area. Regenerated to a new position upon arrival.
    """

    def __init__(self, pos: tuple[int, int],
                 direction: Direction,
                 maze: MazeAdapter,
                 state: GhostState,
                 scatter_area_top_left: tuple[int, int],
                 scatter_area_bottom_right: tuple[int, int]) -> None:
        """Initializes a new Ghost instance.

        Args:
            pos (tuple[int, int]): Initial grid coordinates (x, y).
            direction (Direction): Initial facing direction.
            maze (MazeAdapter): Maze instance for walkability checks.
            state (GhostState): Initial behavioral state.
            scatter_area_top_left (tuple[int, int]): Coordinates (x, y)
                of the scatter zone's top left corner.
            scatter_area_bottom_right (tuple[int, int]): Coordinates (x, y)
                of the scatter zone's bottom right corner.

        Returns:
            None
        """

        super().__init__(pos, direction)
        self.maze = maze
        self.state = state
        self.scatter_area_top_left = scatter_area_top_left
        self.scatter_area_bottom_right = scatter_area_bottom_right
        self.scatter_target = (
            self.generate_random_pos(scatter_area_top_left,
                                     scatter_area_bottom_right))

    def generate_random_pos(self,
                            top_left_boundary: tuple[int, int],
                            bottom_right_boundary: tuple[int, int]
                            ) -> tuple[int, int]:
        """Generates a random target coordinate within specified boundaries.

        Repeats selection until a position distinct from the
            ghost's current position is chosen.

        Args:
            top_left_boundary (tuple[int, int]): Top-left (x, y) coordinates of
                the area boundary.
            bottom_right_boundary (tuple[int, int]): Bottom-right (x, y)
                coordinates of the area boundary.

        Returns:
            tuple[int, int]: A random (x, y) coordinate within the
                designated area.
        """

        target = self.pos

        while target == self.pos:
            x = randint(top_left_boundary[0],
                        bottom_right_boundary[0])
            y = randint(top_left_boundary[1],
                        bottom_right_boundary[1])

            if self.maze.is_reachable((x, y)):
                target = (x, y)

        return target

    def calculate_target(self, pacman_pos: tuple[int, int],
                         pacman_direction: Direction,
                         blinky_pos: tuple[int, int] | None = None
                         ) -> tuple[int, int]:
        """Calculates the target coordinate based on the ghost's current state.

        Args:
            pacman_pos (tuple[int, int]): Current (x, y)
                coordinates of Pacman.
            pacman_direction (Direction): Current direction
                Pacman is facing.
            blinky_pos (tuple[int, int] | None, optional): Current (x, y)
                coordinates of Blinky,
                used for specific ghost AI calculations. Defaults to None.

        Returns:
            tuple[int, int]: The target (x, y) coordinates for navigation.
        """

        if self.state == GhostState.CHASE:
            return self.calculate_chase_target(pacman_pos,
                                               pacman_direction,
                                               blinky_pos)
        elif self.state == GhostState.SCATTER:
            return self.scatter_target
        elif self.state == GhostState.FRIGHTENED:
            return self.generate_random_pos((0, 0), (self.maze.width - 1,
                                                     self.maze.height - 1))

        return self.pos

    def calculate_chase_target(self, pacman_pos: tuple[int, int],
                               pacman_direction: Direction,
                               blinky_pos: tuple[int, int] | None = None
                               ) -> tuple[int, int]:
        """Calculates the target coordinate when in the CHASE state.

        Must be overridden by subclasses to define specific AI behavior.

        Args:
            pacman_pos (tuple[int, int]): Current (x, y)
                coordinates of Pacman.
            pacman_direction (Direction): Current direction
                Pacman is facing.
            blinky_pos (tuple[int, int] | None, optional): Current (x, y)
                coordinates of Blinky, required for certain ghost
                behaviours. Defaults to None.

        Returns:
            tuple[int, int]: The calculated target (x, y) coordinates.

        Raises:
            ValueError
        """

        raise ValueError("The chase method was not implemented")

    def decide_direction(self,
                         pacman_pos: tuple[int, int],
                         pacman_direction: Direction,
                         blinky_pos: tuple[int, int] | None = None
                         ) -> Direction:
        """Determines the next movement direction toward the target cell.

        Evaluates surrounding walkable neighbor cells using
            Manhattan distance to the active target.
        Avoids immediate u turn reversals unless blocked in a dead end.
        Regenerates scatter targets dynamically upon arrival.

        Args:
            pacman_pos (tuple[int, int]): Current (x, y) coordinates of Pacman.
            pacman_direction (Direction): Current facing direction of Pacman.
            blinky_pos (tuple[int, int] | None, optional): Current (x, y)
                coordinates of Blinky, used for team-based target calculations.
                Defaults to None.

        Returns:
            Direction: The chosen direction for the ghost's next move.
        """

        if self.state == GhostState.EATEN:
            return self.direction

        if (self.state == GhostState.SCATTER
           and self.pos == self.scatter_target):
            self.scatter_target = self.generate_random_pos(
                self.scatter_area_top_left,
                self.scatter_area_bottom_right)

        target = self.calculate_target(pacman_pos,
                                       pacman_direction,
                                       blinky_pos)

        opposite_direction = Direction(
            (self.direction.value) % (len(Direction)))

        best_direction: Direction | None = None
        best_distance = float("inf")

        for direction in Direction:
            if direction == opposite_direction:
                continue

            possible_position = self.get_next_position_on(self.pos, direction)

            if not self.maze.is_walkable(self.pos, possible_position):
                continue

            distance = (abs(possible_position[0] - target[0])
                        + abs(possible_position[1] - target[1]))

            if distance < best_distance:
                best_distance = distance
                best_direction = direction

        if best_direction is None:
            best_direction = opposite_direction

        return best_direction

    def update_ghost(self, delta: float,
                     pacman_pos: tuple[int, int],
                     pacman_direction: Direction,
                     blinky_pos: tuple[int, int] | None = None) -> None:
        """Updates the ghost's direction and position for the current frame.

        Decides a new direction when the ghost finishes moving into its
            current cell.
        Then calls the parent update method to advance movement.

        Args:
            delta (float): Movement step delta value.
            pacman_pos (tuple[int, int]): Current (x, y) coordinates of Pacman.
            pacman_direction (Direction): Current direction Pacman is facing.
            blinky_pos (tuple[int, int] | None, optional): Current (x, y)
                coordinates of Blinky, needed for certain targeting logic.
                Defaults to None.

        Returns:
            None
        """

        if self.move_progress <= 0.0:
            next_direction = self.decide_direction(
                pacman_pos, pacman_direction, blinky_pos)
            self.set_next_direction(next_direction)

        self.update(delta, self.maze)
