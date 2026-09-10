"""Adapter module for maze generation and cell navigation."""

from mazegenerator.mazegenerator import MazeGenerator


class Cell():
    """
    Represents a single maze cell with passage states for each direction.

    Attributes:
        n (int): North wall state (1 for wall activated, 0 otherwise).
        e (int): East wall state.
        s (int): South wall state.
        w (int): West wall state.
    """

    def __init__(self, n: int, e: int, s: int, w: int) -> None:
        """
        Initializes a maze cell.

        Args:
            n (int): North direction bit state.
            e (int): East direction bit state.
            s (int): South direction bit state.
            w (int): West direction bit state.

        Returns:
            None
        """

        self.n = n
        self.e = e
        self.s = s
        self.w = w


class MazeAdapter():
    """
    Adapter wrapper around MazeGenerator to provide structured grid access.

    Attributes:
        width (int): Maze width in grid units.
        height (int): Maze height in grid units.
        maze (list[list[Cell]]): Grid matrix containing Cell instances.
    """

    def __init__(self, size: tuple[int, int], seed: int) -> None:
        """
        Initializes the adapter, generates the maze, and builds the Cell grid.

        Args:
            size (tuple[int, int]): Maze dimensions as (width, height).
            seed (int): Random seed for maze generation.

        Returns:
            None
        """

        self.__mazegenerator = MazeGenerator(size=size, seed=seed)
        maze = self.__mazegenerator.maze
        self.width = size[0]
        self.height = size[1]

        self.maze: list[list[Cell]] = []
        for row in range(self.height):
            current_row: list[Cell] = []
            for col in range(self.width):
                current_cell = maze[row][col]
                current_row.append(Cell(
                    (current_cell >> 0) & 1,
                    (current_cell >> 1) & 1,
                    (current_cell >> 2) & 1,
                    (current_cell >> 3) & 1))
            self.maze.append(current_row)

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Retrieves the cell at the given grid coordinates.

        Args:
            x (int): Horizontal cell coordinate (column).
            y (int): Vertical cell coordinate (row).

        Returns:
            Cell: The Cell instance at position (x, y).
        """

        return self.maze[y][x]

    def regenerate(self, seed: int) -> None:
        """
        Regenerates the maze grid using a new random seed.

        Args:
            seed (int): New random seed for maze generation.

        Returns:
            None
        """

        self.__mazegenerator.generate(seed)
        self.maze: list[list[Cell]] = []
        for row in range(self.height):
            current_row: list[Cell] = []
            for col in range(self.width):
                current_cell = self.__mazegenerator.maze[row][col]
                current_row.append(Cell(
                    (current_cell >> 0) & 1,
                    (current_cell >> 1) & 1,
                    (current_cell >> 2) & 1,
                    (current_cell >> 3) & 1))
            self.maze.append(current_row)

    def is_reachable(self, pos: tuple[int, int]) -> bool:
        """Checks whether a given grid position is accessible.

        A position is considered unreachable if it is invalid/None
            or if its completely surrounded by walls on all four sides.

        Args:
            pos (tuple[int, int]): The (x, y) grid coordinates to check.

        Returns:
            bool: True if the position can be reached, False otherwise.
    """

        if not pos:
            return False
        if pos[0] < 0 or pos[0] >= self.width:
            return False
        if pos[1] < 0 or pos[1] >= self.height:
            return False

        cell = self.get_cell(pos[0], pos[1])

        if cell.n and cell.e and cell.s and cell.w:
            return False
        return True

    def is_walkable(self, current_pos: tuple[int, int],
                    next_pos: tuple[int, int]) -> bool:
        """
        Checks if movement between two adjacent positions is valid.

        Args:
            current_pos (tuple[int, int]): Starting grid coordinate (x, y).
            next_pos (tuple[int, int]): Target grid coordinate (x, y).

        Returns:
            bool: True if movement is allowed, False otherwise.
        """

        if not current_pos or not next_pos:
            return False
        if next_pos == current_pos:
            return False
        if not self.is_reachable(next_pos):
            return False

        if next_pos[0] < 0 or next_pos[0] >= self.width:
            return False
        if next_pos[1] < 0 or next_pos[1] >= self.height:
            return False

        current_cell = self.get_cell(current_pos[0], current_pos[1])
        next_cell = self.get_cell(next_pos[0], next_pos[1])

        if current_pos[0] == next_pos[0]:
            # Going upwards
            if current_pos[1] == next_pos[1] + 1:
                return not (current_cell.n or next_cell.s)
            # Going downwards
            else:
                return not (current_cell.s or next_cell.n)
        else:
            # Going left
            if current_pos[0] == next_pos[0] + 1:
                return not (current_cell.w or next_cell.e)
            # Going right
            else:
                return not (current_cell.e or next_cell.w)
