'''
Module name: Maze Generation and Solving

Description:
    The following module generates and solve mazes via the depth
    first search (DFS) approach. Mazes are generated as png images using the
    Python Imaging Library (PIL), and similarly solved by reading in a png
    image, and outputing a new one with the solution marked out in green.
    
'''
import time
import random
from PIL import Image


def get_colors():
    '''
    Colors map that the maze will use:
        0 - Black - A wall
        1 - White - A space to travel in the maze
        2 - Green - A valid solution of the maze
        3 - Red - A backtracked position during maze solving
        4 - Blue - Start and Endpoints of the maze

    **Returns**

        color_map: *dict, int, tuple*
            A dictionary that will correlate the integer key to
            a color.
    '''
    return {
        0: (0, 0, 0),
        1: (255, 255, 255),
        2: (0, 255, 0),
        3: (255, 0, 0),
        4: (0, 0, 255),
    }


def save_maze(maze, blockSize=10, name="maze"):
    '''
    This will save a maze object to a file.

    **Parameters**

        maze: *list, list, int*
            A list of lists, holding integers specifying the different aspects
            of the maze:
                0 - Black - A wall
                1 - White - A space to travel in the maze
                2 - Green - A valid solution of the maze
                3 - Red - A backtracked position during maze solving
                4 - Blue - Start and Endpoints of the maze
        blockSize: *int, optional*
            How many pixels each block is comprised of.
        name: *str, optional*
            The name of the maze.png file to save.

    **Returns**

        None
    '''
    nBlocks = len(maze)
    dims = nBlocks * blockSize
    colors = get_colors()

    # Verify that all values in the maze are valid colors.
    ERR_MSG = "Error, invalid maze value found!"
    assert all([x in colors.keys() for row in maze for x in row]), ERR_MSG

    img = Image.new("RGB", (dims, dims), color=0)

    # Parse "maze" into pixels
    for jx in range(nBlocks):
        for jy in range(nBlocks):
            x = jx * blockSize
            y = jy * blockSize
            for i in range(blockSize):
                for j in range(blockSize):
                    img.putpixel((x + i, y + j), colors[maze[jx][jy]])

    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)


def load_maze(filename, blockSize=10):
    '''
    This will read a maze from a png file into a 2d list with values
    corresponding to the known color dictionary.

    **Parameters**

        filename: *str*
            The name of the maze.png file to load.
        blockSize: *int, optional*
            How many pixels each block is comprised of.

    **Returns**

        maze: *list, list, int*
            A 2D array holding integers specifying each block's color.
    '''
    if ".png" in filename:
        filename = filename.split(".png")[0]
    img = Image.open(filename + ".png")
    dims, _ = img.size
    nBlocks = int(dims / blockSize)
    colors = get_colors()
    color_map = {v: k for k, v in colors.items()}

    maze = [[0 for x in range(nBlocks)] for y in range(nBlocks)]

    for i, x in enumerate(range(0, dims, dims // nBlocks)):
        for j, y in enumerate(range(0, dims, dims // nBlocks)):
            px = x
            py = y
            maze[i][j] = color_map[img.getpixel((px, py))]

    return maze


def pos_chk(x, y, nBlocks):
    '''
    Validate if the coordinates specified (x and y) are within the maze.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the maze.
        y: *int*
            A y coordinate to check if it resides within the maze.
        nBlocks: *int*
            How many blocks wide the maze is.  Should be equivalent to
            the length of the maze (ie. len(maze)).

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (False).
    '''
    return x >= 0 and x < nBlocks and y >= 0 and y < nBlocks


def generate_maze(nBlocks, name="maze", start=(0,0), blockSize=10, slow=False):
    '''
    Generate a maze using the Depth First Search method.

    **Parameters**

        nBlocks: *int*
            The number of blocks in the maze (x and y dims are the same).
        name: *str, optional*
            The name of the output maze.png file.
        start: *tuple, int, optional*
            Where the maze will start from.
        blockSize: *int, optional*
            How many pixels each block will be.
        slow: *bool, optional*
            Whether to save and lag on generation so as to view the mazegen.

    **Returns**

        None
    '''

    # Generate nBlocks x nBlocks matrix
    maze = [
        [0 for i in range(nBlocks)]
        for j in range(nBlocks)
    ]

    # Add start coordinate to the stack
    positions = [start]

    # Define all possible directions
    directions = [
        (0, 1),
        (0, -1),
        (-1, 0),
        (1, 0)
    ]

    # Mark the starting cell as visited
    maze[start[0]][start[1]] = 1

    # Continue DFS while there are still positions in the stack
    while len(positions) > 0:

        # Take the last position in the stack
        x, y = positions[-1]

        # Create empty list for valid directions to be added to
        valid_directions = []

        # Check for valid directions
        for dx, dy in directions:

            # Direction that goes outisde the maze is not valid
            if not pos_chk(x + dx, y + dy, nBlocks):
                continue

            # Direction that goes to a visited cell is not valid
            if maze[x + dx][y + dy] == 1:
                continue

            # Count the number of blocked paths around each potential direction
            blocked_count = 0

            # Count the number of neighboring cells that have been visited
            # around each potential direction
            visited_count = 0

            # Check the neighboring cells around each direction
            for nx, ny in directions:

                # Neighboring cells that are outside the maze add to the
                # blocked path count
                if not pos_chk(x + dx + nx, y + dy + ny, nBlocks):
                    blocked_count += 1

                # Neighboring cells that have been visited adds to the visited
                # cells and blocked paths count
                else:
                    if maze[x + dx + nx][y + dy + ny] == 1:
                        visited_count += 1
                        blocked_count += 1

            # If at least one neighboring cell has already been visited,
            # the direction is not valid. This prevents loops in the maze
            if visited_count > 1:
                continue

            # A direction can have at most two blocked paths to be a valid
            # direction to go in
            if blocked_count < 3:
                valid_directions.append((dx, dy))

        # If there are valid positions
        if len(valid_directions) > 0:

            # Choose a random direction
            dx, dy = random.choice(valid_directions)

            # Move to the cell in the random direction direction
            maze[x + dx][y + dy] = 1

            # Add the coordinate to the stack
            positions.append((x + dx, y + dy))

        # Backtrack if there are no valid positions
        else:
            # Remove the last coordinate from the stack
            positions.pop()

        # If slow is True, lag on generation
        if slow:
            save_maze(maze, blockSize=blockSize, name=name)
            time.sleep(0.1)

    # Save the generated maze
    save_maze(maze, blockSize=blockSize, name=name)


def solve_maze(filename, start=(0, 0), end=(49, 49), blockSize=10, slow=False):
    '''
    Solve a maze using the Depth First Search method.

    **Parameters**

        filename: *str*
            The name of the maze.png file to be solved.
        start: *tuple, int, optional*
            Where the maze will start from.
        end: *tuple, int, optional*
            Where the maze will end.
        blockSize: *int, optional*
            How many pixels each block will be.
        slow: *bool, optional*
            Whether to save and lag on generation so as to view the mazegen.

    **Returns**

        None
    '''
    if ".png" in filename:
        filename = filename.split(".png")[0]
    maze = load_maze(filename, blockSize=blockSize)
    nBlocks = len(maze)

    # Ensure endpoints are always endpoints
    positions = [start]

    # Define all possible directions
    directions = [
        (0, 1),
        (0, -1),
        (-1, 0),
        (1, 0)
    ]

    # This way we ensure the end is colored appropriately.
    # Note - If end is not valid, this solver will fail!
    maze[start[0]][start[1]] = 4
    maze[end[0]][end[1]] = 4

    # Continue DFS while there are still positions in the stack
    while len(positions) > 0:

        # Take position at the top of the stack
        x, y = positions[-1]

        # If the end is reached, break out of the loop
        if (x, y) == end:
            break

        # Iterate through all potential directions
        for dx, dy in directions:

            # If the direction stays within the maze and goes to a unvisited
            # cell, go in that direction.
            if pos_chk(x + dx, y + dy, nBlocks) and maze[x + dx][y + dy] == 1:

                # Move in the direction and mark the cell as a valid path
                maze[x + dx][y + dy] = 2

                # Add the coordinate of the cell to the stack
                positions.append((x + dx, y + dy))

                # Check whether one of the neighboring cells is the endpoint
                for nx, ny in directions:

                    # If the neighboring cell is is the endpoint
                    if (
                        pos_chk(x + dx + nx, y + dy + ny, nBlocks) and
                        maze[x + dx + nx][y + dy + ny] == 4
                    ):

                        # Go in the direction of the endpoint and mark it as a
                        # valid path
                        maze[x + dx + nx][y + dy + ny] = 2

                        # Add the coordinate of the endpoint to the stack to
                        # break out of the loop.
                        positions.append((x + dx + nx, y + dy + ny))

                # Break out of the loop if none of directions are valid
                break

        # Backtrack if there are no valid directions
        else:

            # Mark the cell as backtracked
            maze[x][y] = 3

            # Remove the last coordinate from the stack
            positions.pop()

        # If slow is True, lag on generation
        if slow:
            save_maze(
                maze, blockSize=blockSize, name="%s_solved.png" % filename
                )
            time.sleep(0.1)

    # Display error message if no valid solution
    if not any([m == 2 for row in maze for m in row]):
        print("NO VALID SOLUTION FOR THE CHOSEN ENDPOINT!")

    # Save the solved maze
    save_maze(maze, blockSize=blockSize, name="%s_solved.png" % filename)


if __name__ == "__main__":

    # Generate the maze
    generate_maze(50, start=(0, 0), name="maze", slow=False)

    # Solve the maze
    solve_maze("maze", start=(0, 0), end=(49, 49), blockSize=10, slow=False)
