"""
Lazor Project
"""
import random
from copy import deepcopy as dc
from math import factorial as f

class block:
    """
    Class object that captures how blocks in the Lazor game
    relate to each other (equality comparison) and how different
    blocks interact with the lazor
    """

    def __init__(self, type):
        """
        Defines the instrinic attributes of the block such as 
        type of block and position of the block.
        **Parameters**

            type: *int or float*
                The input value to the function
        """

        self.t = type
        self.p = None
        self.fixed = False

    def __eq__(self, other):
        """
        Defines how to relate blocks using its position by an 
        equality comparison.

        **Parameters**

            other: *block*
                The block being compared to the base block

        **Returns**

            value: *bool*
                The boolean value of if the two blocks are 
                the same.
        """

        if type(other) == block:
            return self.p == other.p and self.t == other.t
        return False

    def reflection(self, L, pc):
        """
        The reflection object determines how a lazor will
        change after reflecting on a block. 

        **Parameters**

            x: *int or float*
                The input value to the function

        **Returns**

            value: *int or float*
                The value of the function inputed at x
        """
        
        p_slope = abs(L.slope(self.p))
        L_slope = abs(L.v[1]/L.v[0])
        if L_slope < p_slope:
            return lazor(pc, [L.v[0], -L.v[1]])
        else:
            return lazor(pc, [-L.v[0], L.v[1]])

    def lazor_interaction(self, L, pc):
        """
        Function determines what lazors are formed from a lazor
        interacting with a block

        **Parameters**

            L: *lazor*
                The lazor that is being looked at
            pc: *list*
                The position of the collision

        **Returns**

            L: *lazor*
                The original lazor with an ending point
            Ls: *list*
                List of lazors that are created from collision
        """
        if L.pi == pc:
            L.pf = pc
            return L, []
        elif self.t == 'A': #reflect
            L.pf = pc #point of contact
            return L, [self.reflection(L, pc)]
        elif self.t == 'B': #opaque
            L.pf = pc #stops here
            return L, []
        elif self.t == 'C': #refract
            L.pf = pc #goes past this block to find new stop point
            return L, [self.reflection(L, pc), L.refract(pc)]


class lazor:
    """
    Class describes how a lazor relate to other lazors,
    as well as helper function that help determine the 
    slope and a new lazor that would form from a 
    refraction.
    """
        
    def __init__(self, inital_p, direction):
        """
        Intrinsic attributes of the lazor

        **Parameters**

            inital_p: *list*
                The starting position of the lazor
            direction: *list*
                The slope of the lazor

        **Returns**

            value: *int or float*
                The value of the function inputed at x
        """
        
        self.pi = [int(inital_p[0]), int(inital_p[1])]
        self.v = [int(direction[0]), int(direction[1])]
        self.pf = None

    def __eq__(self,other):
        """
        Describes the equality of lazors to each other

        **Parameters**

            other: *lazor*
                The opposing lazor being compared

        **Returns**

            value: *bool*
                Boolean value that determines if lazors are
                the same.
        """
        
        return self.pi == other.pi and self.v == other.v

    #really just for refract block to define a new lazor
    def refract(self, pc):
        """
        Describes how a new lazor is formed from
        refracting.

        **Parameters**

            pc: *list*
                Location of the base lazor that will be
                used to define this new lazor

        **Returns**

            L: *lazor*
                The new lazor that is created from a refracting
                block
        """
        
        new_pi = [pc[0] + self.v[0], pc[1] + self.v[1]]
        return lazor(new_pi, self.v)

    def slope(self, p):
        """
        Returns the slope of a point assuming the point
        describes the vertical and horizontal component 
        of the slope.

        **Parameters**

            p: *list*
                A list of the vertical and horizontal 
                components of the slope.

        **Returns**

            value: *int or float*
                The value of the slope
        """
        
        if (p[0] - self.pi[0]) == 0:
            return float('inf')
        return (p[1] - self.pi[1]) / (p[0] - self.pi[0])


class lazor_game:
    """
    This class reads a board file of a level and then is able to solve
    for the correct placement of the blocks.
    """
        
    def __init__(self,board_file):
        """
        Define the intrinic attributes of the lazor_game
        class.

        **Parameters**

            board_file: *str*
                The name of the level file that will be solved
        """
        
        self.b_list = []
        self.l_list = []
        self.goals = 0
        self.read_board_file(board_file)

    #reads input board file and translate it into code
    def read_board_file(self, board_file):
        """
        Reads bff file that describes lazor game and puts it into
        a readable format.

        **Parameters**

            board_file: *str*
                The filename of the input board file
        """
        
        if not board_file.endswith('.bff'):
            board_file += '.bff'

        read_grid = False
        raw_grid, goals = [], []
        with open(board_file) as board:
            for line in board:        
                if line[0] == 'G': #reading grid
                    read_grid = (line[5:10] == 'START')

                elif read_grid: #adding grid
                    raw_grid.append(line.split())

                elif line[0] == 'A': #reflect
                    for i in range(int(line[2])):
                        self.b_list.append(block('A'))

                elif line[0] == 'B': #opaque
                    for i in range(int(line[2])):
                        self.b_list.append(block('B'))

                elif line[0] == 'C': #refract
                    for i in range(int(line[2])):
                        self.b_list.append(block('C'))

                elif line[0] == 'L': #lazor
                    L, x, y, vx, vy = line.split()
                    self.l_list.append(lazor([x, y], [vx, vy]))

                elif line[0] == 'P': #goals
                    goals.append([int(line[2]),int(line[4])])
        board.close()

        self.goals = len(goals)
        self.create_grid(raw_grid, goals)


    #creates a proper grid with correct notation
    def create_grid(self, raw_grid, goals):
        """
        Creates the grid of the level in a fashion that will
        make solving the level easier.

        **Parameters**

            raw_grid: *list*
                Nested list of how grid looks in the orginal
                format
            goals: *list*
                List of the positions of the goals
        """
        
        self.grid = [[0]*(2*len(raw_grid[0])+1) for i in range(2*len(raw_grid)+1)]
        
        for i in range(len(raw_grid)):
            for j in range(len(raw_grid[i])):
                x, y = 2 * i + 1, 2 * j + 1
                if raw_grid[i][j] == "o":
                    self.grid[x][y] = 1 #possible center of block
                elif raw_grid[i][j] == "x":
                    self.grid[x][y] = 7 #blocks cannot be here
                else:
                    b = block(raw_grid[i][j])
                    b.fixed = True
                    self.grid[x][y] = b
                    self.block_place(self.grid, self.grid[x][y], [y, x])

        for y, x in goals:
            self.grid[x][y] = 3

    def out_bounds(self, x, y):
        """
        Determines if position is outside of grid.

        **Parameters**

            x: *int or float*
                The x position
            y: **
                The y position

        **Returns**

            value: *bool*
                The boolean value of if position is outside
                the grid
        """
        
        return x < 0 or x >= len(self.grid) or y >= len(self.grid[0]) or y < 0

    def determine_block(self, grid, p, L):
        """
        Determines what block the lasor might be reflecting off
        of.

        **Parameters**

            p: *list*
                Position of the lazor at its current step
            L: *lazor*
                The lazor that is being looked at

        **Returns**

            value: *bool*
                Boolean value that determines if the lazor
                is reflecting off a block
            b: *block*
                Returns the block that is being reflected
        """
        
        y1, x1 = p
        x2, y2 = x1 + L.v[1], y1 + L.v[0]
        b, b1, b2 = [], [], [] #holds nearby blocks

        #using the next step of the position to determine what block it hits
        ps1 = [[x1 + 1,y1], [x1 - 1, y1], [x1, y1 + 1], [x1, y1 - 1]]
        ps2 = [[x2 + 1,y2], [x2 - 1, y2], [x2, y2 + 1], [x2, y2 - 1]]
        for i in range(4):
            i1, j1 = ps1[i]
            i2, j2 = ps2[i]
            if not self.out_bounds(i1, j1):
                if type(grid[i1][j1]) == block:
                    b1.append(grid[i1][j1])
            if not self.out_bounds(i2, j2):
                if type(grid[i2][j2]) == block:
                    b2.append(grid[i2][j2])

        #determines block by finding the common block
        for i in b1:
            for j in b2:
                if i == j:
                    b.append(i)
                    
        if len(b) < 1: #no block collision
            return False, None
        elif len(b) == 1:
            return True, b[0]

    def push_lazors(self, grid, Ls):
        """
        Determines how the lazors' trajectory will
        change with the current position of the
        blocks.

        **Parameters**

            Ls: *list*
                A list of the lazors in their current positions

        **Returns**

            value: *bool*
                Returns boolean value of if the game is over
                or not.
        """
        
        #goes until all lazors find their end point
        while len(Ls) != 0: 
            L = Ls[0]
            y, x = L.pi
            done = False
            collision = [2,4,6]
            while not done: #push lazors to end point
                t_value, b = self.determine_block(grid, [y, x], L)
                grid_value = grid[x][y]

                #collision is occuring
                if grid_value in collision and t_value:
                    if grid_value == 4:
                        grid[x][y] = 6
                    L, hit = b.lazor_interaction(L, [y, x])
                    Ls.remove(L)
                    done = True
                    for i in hit:
                        Ls.append(i)
                else:
                    #lazor current step is pushed forward
                    if grid_value == 3: #passes goal
                        grid[x][y] = 5
                    x, y = x + L.v[1], y + L.v[0]
                    if self.out_bounds(x, y): #checks for out of bound
                        L.pf = [y - L.v[0], x - L.v[1]]
                        done = True
                        Ls.remove(L)
        return self.check_win(grid)

    def check_win(self, grid):
        """
        Determines if the game is won by seeing if the lazor
        hits all the goals.

        **Parameters**

            grid: *list*
                A nested list that describes how the grid of the
                game looks like for this current iteration.

        **Returns**

            value: *bool*
                Returns True if game is won and False if the 
                game is lost.
        """
        
        win = 0
        b_list = []
        for row in grid:
            for value in row:
                if value == 5 or value == 6: #means lazor passes through
                    win += 1
                elif type(value) == block:#collecting the blocks
                    b_list.append(value)

        if win == self.goals:
            raw_grid = self.grid_game_form(grid)
            with open('solutions.txt', 'w') as sol:
                for b in b_list:
                    x = int((b.p[1] - 1) / 2)
                    y = int((b.p[0] - 1) / 2)
                    self.raw_grid[x][y] = b.t

                sol.write('Congratulations! You won! \n')
                sol.write('\n')
                for row in raw_grid:
                    sol.write('%s \n' % row)
                sol.close()
            return True
        else:
            return False

    def grid_game_form(self, grid):
        """
        ffff


        """

        raw_grid = [[0]*((len(grid)-1)/2) for i in range((len(grid)-1)/2)]
        for i in range(len(grid)):
            for j in range(len(grid)):
                x, y = (i-1)/2, (j-1)/2
                if type(grid[i][j]) == block:
                    raw_grid[x][y] = grid[i][j].t
                elif grid[i][j] == 1:
                    raw_grid[x][y] = 'o'
                elif grid[i][j] == 7:
                    raw_grid[x][y] = 'x'
        return raw_grid

    #function to place block
    def block_place(self, grid, b, p):
        """
        The function assigns a block to a location on the grid
        so that it can be seen how it impacts the lazor's 
        trajectory.

        **Parameters**

            b: *block*
                The block being given a position
            p: *list*
                The position of the block
        """
        
        y, x = b.p = p
        ps = [[x + 1,y], [x - 1, y], [x, y + 1], [x, y - 1]]
        grid[x][y] = b
        for x, y in ps: #places little marker near block
            if grid[x][y] == 3:
                grid[x][y] = 4
            else:
                grid[x][y] = 2

    def frame(self, pos):
        grid = dc(self.grid)
        b_list = dc(self.b_list)
        for i, b in enumerate(b_list):
            self.block_place(grid, b, pos[i])
        return grid

    def generate_grids(self):
        grids = []
        pos = [] # need to figure this out
        for p in pos:
            self.grids(self.frame(p))
        '''pos = []
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == 1:
                    pos.append([j,i])
        a, b, c = [], [], [], []
        for bl in self.b_list:
            if bl.t == 'A':
                a.append(bl)
            elif bl.t == 'B':
                b.append(bl)
            elif bl.t == 'C':
                c.append(bl)
        total = len(self.raw_grid)*len(self.raw_grid[0])
        print('Worst outcome: ', f(len(pos))/(f(len(a))*f(len(b))*f(len(c))*f(len(total)-len(self.b_list)-len(pos))))'''
        return grids

    def lazor_solver(self):
        """
        This function utilizes an algorithm to solve the lazor
        level that was inputed into the lazor_game class.

        **Returns** (need to figure this out)

            value: *int or float*
                ffff
        """

        grids = self.generate_grids()
        for grid in grids:
            if self.push_lazors(grid, dc(self.t_list)):
                break
        print('Algorithm is done')

if __name__ == "__main__":
    a = lazor_game('tiny_5')
    a.lazor_solver()
