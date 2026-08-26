from maze import MazeAdapter


class GameState:
    def __init__(self, active_screen: str, maze: MazeAdapter):
        self.active_screen = active_screen
        self.maze = maze
        self.in_game = False
