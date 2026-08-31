from parser.parser import parser_configuration_file
from maze.maze_adapter import MazeAdapter
import sys


if __name__ == "__main__":
    configs = parser_configuration_file(sys.argv[1])
    level = configs["level"][0]
    maze = MazeAdapter(size=(level["width"], level["height"]),
                       seed=configs["seed"])
