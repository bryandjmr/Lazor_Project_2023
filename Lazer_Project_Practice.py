class Block:
    def __init__(self, block_type, position, fixed=True):
        self.block_type = block_type
        self.position = position
        self.fixed = fixed

    def interact_with_laser(self, laser):
        """Updates the laser direction based on the type of block and the side of collision.
        For the refract type, it returns an additional laser if needed.
        :param laser: A tuple of (x, y, vx, vy)
        :return: A list of lasers (might contain one or two lasers)"""
        if self.block_type == 'A':
            return [self.reflect(laser)]
        elif self.block_type == 'B':
            return [self.opaque(laser)]
        elif self.block_type == 'C':
            return [self.refract(laser)]
        else:
            return [laser]  # Non-interactive block returns the laser unchanged

    def reflect(self, laser):
        # Logic to reflect the laser
        x, y, vx, vy = laser
        # Assuming we know the side of collision, which needs to be calculated:
        # if collision at left or right side:
        vx *= -1
        # if collision at top or bottom side:
        vy *= -1
        return x, y, vx, vy

    def opaque(self, laser):
        # Logic for opaque block, laser stops
        return None

    def refract(self, laser):
        # Logic for refract block, laser splits
        # Original laser continues in the same direction
        new_laser = self.reflect(laser)
        return [laser, new_laser]  # Return both the unchanged and the reflected lasers

def parse_bff(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    grid = []
    blocks = {'A': [], 'B': [], 'C': []}  # Dictionaries to hold the blocks by type
    lasers = []
    points = []
    x_size = y_size = 0

    parsing_grid = False
    for line in lines:
        line = line.strip()
        if line == 'GRID START':
            parsing_grid = True
        elif line == 'GRID STOP':
            parsing_grid = False
        elif parsing_grid:
            grid.append(list(line))
            y_size += 1
            x_size = max(x_size, len(line))
        elif line and line[0] in 'ABC':
            block_type, quantity = line.split()
            # Fill in the blocks dictionary with the number of each block type
            blocks[block_type] = [Block(block_type, None, fixed=False) for _ in range(int(quantity))]
        elif line and line[0] == 'L':
            _, x, y, dx, dy = line.split()
            lasers.append((int(x), int(y), int(dx), int(dy)))
        elif line and line[0] == 'P':
            _, x, y = line.split()
            points.append((int(x), int(y)))

    # Process the grid to identify fixed blocks and mark 'X' as non-placeable
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in 'ABC':
                blocks[cell].append(Block(cell, (x, y)))
            elif cell == 'X':
                # This position is not placeable, could be used in future logic
                pass
    non_placeable = set()  # Use a set to store non-placeable positions
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in 'ABC':
                blocks[cell].append(Block(cell, (x, y)))
            elif cell == 'X':
                non_placeable.add((x, y))  # Store the non-placeable position
    # The grid size will be based on the max length of the lines and the number of lines.
    # Pad rows in grid if they are not equal to x_size
    grid = [row + ['o'] * (x_size - len(row)) for row in grid]

    # The grid size will be based on the max length of the lines and the number of lines.
    grid_size = (x_size, y_size)
    """
    #printing block types
    print("Blocks present in the file:")
    for block_type in blocks:
        print(f"{block_type}: {len(blocks[block_type])} blocks")

    # Printing laser directions
    print("\nLasers' directions:")
    for laser in lasers:
        x, y, dx, dy = laser
        print(f"Laser at ({x}, {y}) moving in direction ({dx}, {dy})")

    # Printing points the laser needs to reach
    print("\nPoints the laser needs to reach:")
    for point in points:
        x, y = point
        print(f"Point at ({x}, {y})")
    """
    return grid, blocks, lasers, points, grid_size, non_placeable

# Use the parse_bff function with a given filename
filename = "mad_7.bff"
grid, blocks, lasers, points, grid_size, non_placeable = parse_bff(filename)

"""
def print_grid(grid):
    for row in grid:
        print(' '.join(row))
    print()
print("Grid:")
print_grid(grid)"""

