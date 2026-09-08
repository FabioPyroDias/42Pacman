from maze.maze_adapter import MazeAdapter
import sys


def print_grid(maze: MazeAdapter) -> None:
    """
    Render the maze to the terminal.

    Args:
        None

    Returns:
        None

    This method prints:
        - Walls
        - Entry and exit points
        - Optional solution path
        - Optional "42" pattern

    Notes:
        - Uses ANSI escape codes for coloring.
        - Clears the terminal before rendering.
        - Rendering logic is tightly coupled to grid structure.
    """

    # Although this method seems very confusing the idea is quite simple.
    # Each cell has overlapping walls between them and their neighbours.
    #
    #   W W W    W W W
    #   W   W    W   W
    #   W W W    W W W
    #
    #   W W W    W W W
    #   W   W    W   W
    #   W W W    W W W
    #
    # To avoid repetition, each cells prints
    #   their top left, top, and left wall.
    # The cells in the last column
    #   also print the top right and right wall.
    # The cells in the last row
    #   also print the bottom left and bottom wall.
    #
    # The walls might be closed or open.
    # In case they're open, they might connect cells in the shortest
    #   solved path.
    # A check is needed to change the render in that space
    #
    #   W P W    W W W
    #   W   P    P   W
    #   W W W    W P W
    #
    #   W W W    W P W
    #   W   P    P   W
    #   W P W    W W W
    #
    # Cell render priority:
    # Each cell can be:
    # - Entry
    # - Exit
    # - Path
    # - 42 Pattern
    # - Slot
    #
    # To avoid repeating prints, a simple if/elif/else condition is made:
    # First check if the cell is the maze entry followed by the maze exit
    # Next if it's in the shortest path, followed by the 42 pattern
    # And finally, if none of these are true, print it as a normal cell.

    row = 0
    while row < maze.height:
        col = 0
        # Print the top walls
        while col < maze.width:
            # Print the top left wall
            # print("\033[97;107m\u2588\033[0m", end="")
            print("#", end="")

            # In case there's a wall, print it.
            # Otherwise:
            # 1. Check if display path is active and if the cell is
            #   in the path. If so:
            #   1.1. Check wether the cell is in the beginning of the path,
            #       the end or in between.
            #   1.2. If the previous cell, next cell or both cells "row"
            #       coordinate is minus 1 unit.
            #       This means the open wall between the current and
            #           the neighbour cell is part of the path
            if maze.get_cell(col, row).n:
                # print("\033[97;107m\u2588\033[0m", end="")
                print("#", end="")
            else:
                # If the wall is open but the current cell
                #   doesn't belong to the path, print the open wall.
                print(" ", end="")

            # Reached the final column, needs to print the top right wall.
            if col == maze.width - 1:
                # print("\033[97;107m\u2588\033[0m")
                print("#")
            col += 1

        col = 0
        while col < maze.width:
            cell = maze.get_cell(col, row)

            # Print the left wall
            if cell.w:
                # print("\033[97;107m\u2588\033[0m", end="")
                print("#", end="")
            else:
                # Same logic as before, but this time it's applied to
                # the left wall instead of the upper one.
                print(" ", end="")

            # Print the slot itself.
            if cell.n and cell.e and cell.s and cell.w:
                print("X", end="")
            else:
                print(" ", end="")

            # Reached the final column, needs to print the right wall.
            if col == maze.width - 1:
                # print("\033[97;107m\u2588\033[0m")
                print("#")
            col += 1

        # Reached the final row, needs to print the lower walls.
        if row == maze.height - 1:
            col = 0
            while col < 2 * maze.width + 1:
                # print("\033[97;107m\u2588\033[0m", end="")
                print("#", end="")
                col += 1
            print()
        row += 1


if __name__ == "__main__":
    maze = MazeAdapter(size=(int(sys.argv[1]),
                             int(sys.argv[2])),
                       seed=int(sys.argv[3]))

    pattern_42 = []

    for row in range(maze.height):
        for col in range(maze.width):
            cell = maze.get_cell(col, row)
            if cell.n and cell.e and cell.s and cell.w:
                pattern_42.append((col, row))

    print("Pattern 42: ")
    for cell in pattern_42:
        print(f"Cell: {cell}")
    print()
    print_grid(maze)
