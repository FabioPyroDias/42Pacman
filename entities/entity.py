from enums import Direction


class Entity():
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos


class MovableEntity(Entity):
    def __init__(self, pos: tuple[int, int], direction: Direction) -> None:
        super().__init__(pos)
        self.direction = direction
        self.next_direction: Direction | None = None
        self.move_progress: float = 0.0

    def set_next_direction(self, next_direction: Direction) -> None:
        self.next_direction = next_direction

    def get_next_position(self) -> tuple[int, int]:
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

    # Maze needed
    """ def update(self, delta: float, maze: MazeGenerator):
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
                self.move_progress = 1.0 - self.move_progress
            else:
                self.move_progress += delta

        if self.move_progress >= 1.0:
            self.pos = self.get_next_position()
            self.move_progress = 0.0 """
