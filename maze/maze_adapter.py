from mazegenerator.mazegenerator import MazeGenerator
from typing import TypedDict


class Cell(TypedDict):
    N: int
    L: int
    S: int
    W: int


class MazeAdapter():
    def __init__(self, size: tuple[int, int] = (15, 15),
                 seed: int = 0) -> None:
        self.maze = MazeGenerator(size=size, seed=seed).maze
        self.width = size[0]
        self.height = size[1]

    def get_cell(self, x: int, y: int) -> Cell:
        return {"N": (self.maze[y][x] >> 0) & 1,
                "L": (self.maze[y][x] >> 1) & 1,
                "S": (self.maze[y][x] >> 2) & 1,
                "W": (self.maze[y][x] >> 3) & 1}
