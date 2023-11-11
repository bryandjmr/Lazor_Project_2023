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
                   movable_blocks.append(Block(block_type, None))  # None for position since it's movable
                   
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
                fixed_blocks.append(Block(cell, (x, y), True))
                grid[y][x] = 'o'  # Optional: Replace the block symbols with something else like 'o'
        
    return grid, movable_blocks, fixed_blocks, lasers, points

if __name__ == "__main__":
    grid, movable_blocks, fixed_blocks, lasers, target_points = parse_bff('tiny_5.bff')