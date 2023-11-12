class Block:

    def __init__(self, block_type, position, fixed=False):
        self.block_type = block_type
        self.position = position
        self.fixed = fixed

    def interact_with_laser(self, laser):
        if self.block_type == 'A':
            laser.reflect()  # Reflect method needs to be defined in Laser class
            return [laser],[]  # Only one laser continues, no new laser created.

        elif self.block_type == 'B':
            return [], []  # Laser stops, no lasers continue.

        elif self.block_type == 'C':
            through_laser = Laser(laser.position, laser.direction)
            reflect_laser = Laser(laser.position, (laser.direction[1],-laser.direction[0]))
            return [through_laser],[reflect_laser]

class Laser:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def move(self):
        """Moves the laser one step in its current direction."""
        self.position = (self.position[0] + self.direction[0],
                         self.position[1] + self.direction[1])
        
    def reflect(self):
        """Reflects the laser's direction by 90 degrees, simulating a 45-degree
        angle of incidence and reflection with respect to the block's face."""
        self.direction = (self.direction[1], -self.direction[0])
        self.position = (self.position[0] + self.direction[0],
                         self.position[1] + self.direction[1])

def parse_bff(filename):
    """
    Define grid, fixed blocks, movable blocks, lasers and end points.
    
    """

    with open(filename, 'r') as file:
        lines = file.readlines()

    # Initializing lists to hold various elements
    grid = []
    fixed_blocks = {}
    movable_blocks = []
    lasers = []
    points = []

    # Flags to know when to start parsing which part
    parsing_grid = False

    for line in lines:
        line = line.strip()

        if line == 'GRID START':
            parsing_grid = True

        elif line == 'GRID STOP':
            parsing_grid = False
            #parsing_blocks = True  # Assuming blocks are listed right after the grid

        elif parsing_grid and line:
            grid.append(list(line))

        elif line.startswith(('A', 'B', 'C')):  # Assuming 'A', 'B', 'C' are blocks
                block_type, quantity = line.split()
                for _ in range(int(quantity)):
                   movable_blocks.append((block_type, Block(block_type, None)))  # None for position since it's movable
                   
        elif line.startswith('L'):
            line = line[1:]
            x, y, dx, dy = map(int,line.split())
            lasers.append((x, y, dx, dy))
    
        elif line.startswith('P'):
            line = line[1:]
            if line:  # Assuming points lines are not empty
                points.append(tuple(map(int, line.split())))

    # Convert grid symbols to Block objects for fixed blocks
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in 'ABC':
                fixed_blocks[(x,y)] = Block(cell, (x, y), True)
                grid[y][x] = cell  # Optional: Replace the block symbols with something else like 'o'
    grid = [[cell for cell in row if cell != ' '] for row in grid]
    
    return grid, movable_blocks, fixed_blocks, lasers, points


def simulate_lasers(grid, config, lasers):
    """This function will take the current grid configuration and simulate the path
    of all lasers according to the block interactions."""
    laser_paths = []
    for laser_info in lasers:
        # Create a Laser object from the laser_info tuple
        laser = Laser(position=(laser_info[0], laser_info[1]), direction=(laser_info[2], laser_info[3]))
        path = trace_laser_path(grid, config, laser)
        laser_paths.append(path)
    return laser_paths

def trace_laser_path(grid, config, laser):
    """Trace the path of a single laser given the grid and block configuration."""
    path = []

    while True:
        # Move the laser one step
        laser.move()
        next_position = laser.position

        # Check if next position is outside the grid
        if not is_position_inside_grid(next_position, grid):
            break

        if next_position in config.keys():  # If there's a block at the position
            block = config[next_position]
            result = block.interact_with_laser(laser)
            continuing_lasers, new_lasers = result
            path.append(next_position)  # Add the interaction point to the path
            # Handle continuing lasers
            for lsr in continuing_lasers:
                path += trace_laser_path(grid, config, lsr)  # Recursively trace the path of the continuing laser
            # Handle new lasers created by refraction, if any
            for lsr in new_lasers:
                path += trace_laser_path(grid, config, lsr)  # Recursively trace the path of the new laser
            break  # Once a block is encountered, we stop the current laser
        
        path.append(next_position) # If there's no block, just add the position to the path

    return path

def is_position_inside_grid(position, grid):
    """Check if a given position is inside the boundaries of the grid."""
    rows = len(grid[0])*2
    cols = len(grid[1])*2
    x, y = position
    return 0 <= x <= cols and 0 <= y <= rows

def check_all_target_points_met(target_points, laser_paths):
    """ Check if all target points are hit by the lasers."""
    # Flatten the list of laser paths to a set of points
    points_hit = set(pt for path in laser_paths for pt in path)
    return all(point in points_hit for point in target_points)

def is_solution(grid, config, target_points):
    # Simulate lasers and check if all target_points are intersected
    laser_paths = simulate_lasers(grid, config, lasers)
    return check_all_target_points_met(target_points, laser_paths)

def get_possible_positions(grid, fixed_blocks, movable_blocks, remaining_blocks, movable_config={}, configs_list=[]):

    # Base case: if no more blocks to place, print the current configuration
    if remaining_blocks == 0:
        config = {**fixed_blocks, **movable_config}
        return

    # Iterate over all cells in the grid
    for i in range(len(grid[0])):
        for j in range(len(grid[1])):
            # Check if the cell is empty and not a fixed block position
            if (i, j) not in fixed_blocks.keys() and (i, j) not in movable_config.keys():

                # Place a block in the current cell
                movable_config[(i,j)] = movable_blocks[remaining_blocks-1][1]

                # Recursively generate configurations for the remaining blocks
                get_possible_positions(grid, fixed_blocks, movable_blocks, remaining_blocks - 1, movable_config)

                # Backtrack by removing the last block placed
                movable_config.popitem()
                
    return configs_list
        
def expand_block_coordinate(grid, config):

    expand_config = {}
    
    for position, block in config.items():
        x, y = position[0], position[1]
        expand_config[(x*2+1,y*2)] = block
        expand_config[(x*2,y*2+1)] = block
        expand_config[(x*2+2,y*2+1)] = block
        expand_config[(x*2+1,y*2+2)] = block
    
    return(expand_config)

def solve_lazor_puzzle(grid, movable_blocks, fixed_blocks, lasers, target_points, n=1):
    configs_list = get_possible_positions(grid, fixed_blocks, movable_blocks, len(movable_blocks))
   
    pass

if __name__ == "__main__":
    grid, movable_blocks, fixed_blocks, lasers, target_points = parse_bff('tiny_5.bff')

    # solve_lazor_puzzle(grid, movable_blocks, fixed_blocks, lasers, target_points)
    
    