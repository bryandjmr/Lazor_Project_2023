#maybe create subclasses that react to the lazor differently (option 1)
#or build in that into the block class (option 2)
class Block:
    def __init__(self, block_type, position, fixed=False):
        self.block_type = block_type
        self.position = position
        self.fixed = fixed
    def interact_with_laser(self, laser):
        if self.block_type == 'reflect':
            laser.reflect()  # Reflect method needs to be defined in Laser class
            return [laser], []  # Only one laser continues, no new laser created.
        elif self.block_type == 'opaque':
            return [], []  # Laser stops, no lasers continue.
        elif self.block_type == 'refract':
            through_laser = Laser(laser.position, laser.direction)
            reflect_laser = Laser(laser.position, self._reflect_direction(laser.direction))
            return [through_laser], [reflect_laser]
        return [laser], []
    def _reflect_direction(self, direction):
        vx, vy = direction
        return (-vy, vx)  # For a 90-degree reflection
class Laser:
    def __init__(self, position, direction):
        self.position = position  # A tuple (x, y)
        self.direction = direction  # A tuple (vx, vy) indicating direction

    def move(self):
        """Moves the laser one step in its current direction."""
        self.position = (self.position[0] + self.direction[0],
                         self.position[1] + self.direction[1])
    def reflect(self):
        """Reflects the laser's direction by 90 degrees, simulating a 45-degree
        angle of incidence and reflection with respect to the block's face."""
        vx, vy = self.direction
        # For a 45-degree block, the reflection swaps the x and y components of the velocity,
        # and reverses the sign of one of them. Which one depends on the block's orientation,
        # but since we don't have that information, we'll assume the simplest case:
        self.direction = (vy, -vx)
#The function opens the .bff file, iterates over each line, and depending on the content
#it populates different variables that hold the grid, the blocks, the lasers, and the points
#Need to replace 'path_to_your_file.bff' with the actual path to the file
def parse_bff(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Initializing lists to hold various elements
    grid = []
    fixed_blocks = []
    movable_blocks = []
    lasers = []
    points = []
    # Flags to know when to start parsing which part
    parsing_grid = False
    parsing_blocks = False
    parsing_lasers = False
    parsing_points = False
    for line in lines:
        line = line.strip()
        if line == 'GRID START':
            parsing_grid = True
        elif line == 'GRID STOP':
            parsing_grid = False
            parsing_blocks = True  # Assuming blocks are listed right after the grid
        elif parsing_grid and line:
            grid.append(list(line))
        elif parsing_blocks:
            if line.startswith(('A', 'B', 'C')):  # Assuming 'A', 'B', 'C' are blocks
                block_type, quantity = line.split()
                for _ in range(int(quantity)):
                    movable_blocks.append(Block(block_type, None))  # None for position since it's movable
            elif line.startswith('L'):
                parsing_blocks = False
                parsing_lasers = True
            elif line.startswith('P'):
                parsing_blocks = False
                parsing_points = True
        elif parsing_lasers:
            if line:  # Assuming lasers lines are not empty
                x, y, dx, dy = map(int, line.split())
                lasers.append((x, y, dx, dy))
            else:
                parsing_lasers = False
        elif parsing_points:
            if line:  # Assuming points lines are not empty
                points.append(tuple(map(int, line.split())))
    # Convert grid symbols to Block objects for fixed blocks
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in 'ABC':
                fixed_blocks.append(Block(cell, (x, y), True))
                grid[y][x] = 'o'  # Optional: Replace the block symbols with something else like 'o'
    return grid, movable_blocks, fixed_blocks, lasers, points
def find_fixed_block_positions(block_type, grid):
    fixed_blocks = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == block_type:
                fixed_blocks.append((block_type, (x, y)))
    return fixed_blocks
# Example usage:
grid, movable_blocks,fixed_blocks, lasers, points, *_ = parse_bff('C:\\Users\\victh\\PycharmProjects\\EN.540SoftwareCarpentry\\Lazor_Project_2023\\tiny_5.bff')
print("Grid:")
for row in grid:
    print(row)
print("Blocks:", movable_blocks, fixed_blocks)
print("Lasers:", lasers)
print("Points:", points)
def simulate_lasers(grid, config, lasers):
    """This function will take the current grid configuration and simulate the path
    of all lasers according to the block interactions."""
    laser_paths = []
    for laser_info in lasers:
        # Create a Laser object from the laser_info tuple
        laser = Laser(position=(laser_info[0], laser_info[1]), direction=(laser_info[2], laser_info[3]))
        path = trace_laser_path(grid, laser, config)
        laser_paths.append(path)
    return laser_paths
def trace_laser_path(grid, laser, config):
    """Trace the path of a single laser given the grid and block configuration."""
    path = [laser.position]
    current_position, current_direction = laser.position, laser.direction
    while True:
        # Move the laser one step
        laser.move()
        next_position = laser.position
        # Check if next position is outside the grid
        if not is_position_inside_grid(next_position, grid):
            break
        if next_position in config:  # If there's a block at the position
            block = config[next_position]
            result = block.interact_with_laser(laser)
            continuing_lasers, new_lasers = result
            path.append(next_position)  # Add the interaction point to the path
            # Handle continuing lasers
            for lsr in continuing_lasers:
                path += trace_laser_path(grid, lsr, config)  # Recursively trace the path of the continuing laser
            # Handle new lasers created by refraction, if any
            for lsr in new_lasers:
                path += trace_laser_path(grid, lsr, config)  # Recursively trace the path of the new laser
            break  # Once a block is encountered, we stop the current laser
        path.append(next_position)  # If there's no block, just add the position to the path
    return path
def get_block_interaction_at_position(position, config):
    """Return the block at a given position."""
    return config.get(position)
def is_position_inside_grid(position, grid):
    """Check if a given position is inside the boundaries of the grid."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    x, y = position
    return 0 <= x < cols and 0 <= y < rows
def check_all_target_points_met(target_points, laser_paths):
    """ Check if all target points are hit by the lasers."""
    # Flatten the list of laser paths to a set of points
    points_hit = set(pt for path in laser_paths for pt in path)
    return all(point in points_hit for point in target_points)
# Example usage within the is_solution function
def is_solution(config, target_points):
    # Simulate lasers and check if all target_points are intersected
    laser_paths = simulate_lasers(grid, config, lasers)
    return check_all_target_points_met(target_points, laser_paths)
def can_continue(config, movable_blocks):
    """Determine if the search can continue based on the remaining movable blocks."""
    # Placeholder logic: can continue if there are movable blocks left
    return any(block for block in movable_blocks if not block['placed'])
def generate_next_configs(config, movable_blocks):
    next_configs = []
    for block in movable_blocks:
        if block.position is None:  # Check if the block hasn't been placed
            for new_pos in get_possible_positions(grid):
                new_config = place_block(config, block, new_pos)
                next_configs.append(new_config)
    return next_configs
def get_possible_positions(grid):
    """Return all possible positions where a block could be placed."""
    # Placeholder logic
    return [(x, y) for x in range(len(grid[0])) for y in range(len(grid))]
def place_block(config, block, position):
    new_config = config.copy()
    new_block = Block(block.block_type, position, block.fixed)  # Create a new Block with the updated position
    new_config[position] = new_block
    return new_config
def create_initial_configuration(grid, movable_blocks, fixed_blocks):
    """Create the initial configuration with fixed blocks in place."""
    config = {}
    for block in fixed_blocks:
        config[block.position] = block  # Now storing Block instances
    for block in movable_blocks:
        # No need to set 'placed' because it's already part of Block's __init__
        block.position = None  # Reset position since it's not yet placed
    return config

def solve_lazor_puzzle(grid, movable_blocks, fixed_blocks, lasers, target_points, max_depth):
    def is_solution(config):
        # Simulate lasers and check if all target_points are intersected
        paths, target_points_met = simulate_lasers(grid, config, lasers)
        return all(target_points_met.values())

    def search(config, depth):
        if depth > max_depth:
            return None
        if is_solution(config):
            return config
        for next_config in generate_next_configs(config, movable_blocks):
            result = search(next_config, depth + 1)
            if result:
                return result
        return None

    # Start the search with an initial configuration
    initial_config = create_initial_configuration(grid, movable_blocks, fixed_blocks)
    return search(initial_config, 0)
max_search_depth = 10
# Example usage:
grid, movable_blocks, fixed_blocks, lasers, target_points = parse_bff('C:\\Users\\victh\\PycharmProjects\\EN.540SoftwareCarpentry\\Lazor_Project_2023\\tiny_5.bff')
solution = solve_lazor_puzzle(grid, movable_blocks, fixed_blocks, lasers, target_points, max_search_depth)
if solution:
    print("Solution found!")
    # Code to visualize or output the solution
else:
    print("No solution exists.")