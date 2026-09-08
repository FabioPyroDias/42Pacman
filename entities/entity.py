"""Base entity and movable entity classes for grid-based game objects."""

from enums import Direction
from maze.maze_adapter import MazeAdapter


class Entity():
    """
    Base class representing any object in the game grid.

    Attributes:
        pos (tuple[int, int]): Grid coordinates (x, y) of the entity.
    """

    def __init__(self, pos: tuple[int, int]) -> None:
        """
        Initializes an entity.

        Args:
            pos (tuple[int, int]): Initial grid coordinates (x, y).

        Returns:
            None
        """

        self.pos = pos


class MovableEntity(Entity):
    """
    Entity capable of moving between grid cells with smooth interpolation.

    Attributes:
        direction (Direction): Current active movement direction.
        next_direction (Direction | None): Buffered next direction requested.
        move_progress (float): Progress of current
            position transition (0.0 to 1.0).
        reversing (bool): Flag indicating if the entity is performing
            an immediate "U turn" mid cell.
    """

    def __init__(self, pos: tuple[int, int], direction: Direction) -> None:
        """
        Initializes a movable entity.

        Args:
            pos (tuple[int, int]): Initial grid coordinates (x, y).
            direction (Direction): Initial facing direction.

        Returns:
            None
        """

        super().__init__(pos)
        self.direction = direction
        self.next_direction: Direction | None = None
        self.move_progress: float = 0.0
        self.reversing: bool = False

    def set_next_direction(self, next_direction: Direction) -> None:
        """
        Buffers the next desired direction for turn decisions.

        Args:
            next_direction (Direction): Target direction to switch to.

        Returns:
            None
        """

        self.next_direction = next_direction

    def get_next_position(self) -> tuple[int, int]:
        """
        Calculates the target grid position based on a given direction.

        Args:
            None

        Returns:
            tuple[int, int]: Target coordinates (x, y).
        """

        if not self.next_direction:
            if self.direction == Direction.NORTH:
                return (self.pos[0], self.pos[1] - 1)
            elif self.direction == Direction.SOUTH:
                return (self.pos[0], self.pos[1] + 1)
            elif self.direction == Direction.EAST:
                return (self.pos[0] + 1, self.pos[1])
            elif self.direction == Direction.WEST:
                return (self.pos[0] - 1, self.pos[1])
        else:
            if self.next_direction == Direction.NORTH:
                return (self.pos[0], self.pos[1] - 1)
            elif self.next_direction == Direction.SOUTH:
                return (self.pos[0], self.pos[1] + 1)
            elif self.next_direction == Direction.EAST:
                return (self.pos[0] + 1, self.pos[1])
            elif self.next_direction == Direction.WEST:
                return (self.pos[0] - 1, self.pos[1])
        return (-1, -1)

    def get_next_position_on(self, pos: tuple[int, int],
                             direction: Direction) -> tuple[int, int]:
        """Calculates the neighbour cell position in a given direction.

        Args:
            pos (tuple[int, int]): Starting grid coordinates (x, y).
            direction (Direction): Direction to move from pos.

        Returns:
            tuple[int, int]: The resulting coordinates (x, y).
        """

        if direction == Direction.NORTH:
            return (pos[0], pos[1] - 1)
        elif direction == Direction.SOUTH:
            return (pos[0], pos[1] + 1)
        elif direction == Direction.EAST:
            return (pos[0] + 1, pos[1])
        else:
            return (pos[0] - 1, pos[1])

    def update(self, delta: float, maze: MazeAdapter) -> None:
        """
        Updates movement progress and grid position based on maze walls.

        Args:
            delta (float): Movement step delta value.
            maze (MazeAdapter): Maze instance for walkability checks.

        Returns:
            None
        """

        if self.reversing:
            if (self.next_direction
               and abs(self.direction.value - self.next_direction.value) == 2):
                self.direction = self.next_direction
                self.next_direction = None
                self.reversing = False
            else:
                self.move_progress -= delta
                if self.move_progress <= 0.0:
                    self.move_progress = 0.0
                    self.reversing = False
                return

        if self.move_progress <= 0.0:
            next_position = self.get_next_position()
            if maze.is_walkable(self.pos, next_position):
                if self.next_direction:
                    self.direction = self.next_direction
                    self.next_direction = None
                self.move_progress += delta
        elif self.move_progress > 0.0 and self.move_progress <= 1.0:
            if (self.next_direction
               and abs(self.direction.value - self.next_direction.value) == 2):
                self.direction = self.next_direction
                self.next_direction = None
                self.reversing = True
            else:
                self.move_progress += delta

        if self.move_progress >= 1.0:
            self.pos = self.get_next_position()
            self.move_progress = 0.0
