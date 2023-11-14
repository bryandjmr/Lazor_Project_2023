"""
Lazor Project
"""


class block:
    """
    """
    def __init__(self, type):
        """
        """

        self.t = type
        self.p = None

    def __eq__(self, other):
        """
        """

        if type(other) == block:
            return self.p == other.p
        return False

    #helper function to create a new lazor for reflections
    def reflection(self, L, pc):
        """
        """
        
        p_slope = abs(L.slope(self.p))
        L_slope = abs(L.v[1]/L.v[0])
        if L_slope < p_slope:
            return lazor(pc, [L.v[0], -L.v[1]])
        else:
            return lazor(pc, [-L.v[0], L.v[1]])

    #creates new lazor and gives the original lazor a stopping point
    def lazor_interaction(self, L, pc):
        """
        """
        
        if self.t == 'A': #reflect
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
    """
        
    def __init__(self, inital_p, direction):
        """
        """
        
        self.pi = [int(inital_p[0]), int(inital_p[1])]
        self.v = [int(direction[0]), int(direction[1])]
        self.pf = None

    def __eq__(self,other):
        """
        """
        
        return self.pi == other.pi and self.v == other.v

    #really just for refract block to define a new lazor
    def refract(self, pc):
        """
        """
        
        new_pi = [pc[0] + self.v[0], pc[1] + self.v[1]]
        return lazor(new_pi, self.v)

    #helper function to reduce length of code lines
    def slope(self, p):
        """
        """
        
        if (p[0] - self.pi[0]) == 0:
            return float('inf')
        return (p[1] - self.pi[1]) / (p[0] - self.pi[0])


class lazor_game:
    """
    """
        
    def __init__(self,board_file):
        """
        """
        
        self.block_list = []
        self.lazor_list = []
        self.goals = 0
        self.read_board_file(board_file)

    #reads input board file and translate it into code
    def read_board_file(self, board_file):
        """
        """
        
        if not board_file.endswith('.bff'):
            board_file += '.bff'

        read_grid = False
        raw_grid, goals = [], []
        with open(board_file) as board:
            for line in board:                
                if line[0] == 'G':
                    read_grid = (line[5:10] == 'START')

                elif read_grid:
                    raw_grid.append(line.split())

                elif line[0] == 'A': #reflect
                    for i in range(int(line[2])):
                        self.block_list.append(block('A'))

                elif line[0] == 'B': #opaque
                    for i in range(int(line[2])):
                        self.block_list.append(block('B'))

                elif line[0] == 'C': #refract
                    for i in range(int(line[2])):
                        self.block_list.append(block('C'))

                elif line[0] == 'L': #lazor
                    L, x, y, vx, vy = line.split()
                    self.lazor_list.append(lazor([x, y], [vx, vy]))

                elif line[0] == 'P':
                    goals.append([int(line[2]),int(line[4])])
        board.close()

        self.goals = len(goals)
        self.create_grid(raw_grid, goals)


    #creates a proper grid with correct notation
    def create_grid(self, raw_grid, goals):
        """
        """
        
        self.grid = [[0]*(2*len(raw_grid[0])+1) for i in range(2*len(raw_grid)+1)]
        
        for i in range(len(raw_grid)):
            for j in range(len(raw_grid[i])):
                x, y = 2 * i + 1, 2 * j + 1
                if raw_grid[i][j] == "o":
                    self.grid[x][y] = 1 #possible center of block
                elif raw_grid[i][j] == "x":
                    continue
                else:
                    self.grid[x][y] = block(raw_grid[i][j])
                    self.block_place(self.grid[x][y], [y, x])

        for y, x in goals:
            self.grid[x][y] = 3

    def display(self):
        """
        """
        
        print('Grid: ', self.grid)
        print('Blocks: ', len(self.block_list), self.block_list)
        print('Lazors: ', len(self.lazor_list), self.lazor_list)

    def out_bounds(self, x, y):
        """
        """
        
        return x < 0 or x >= len(self.grid) or y >= len(self.grid[0]) or y < 0

    def determine_block(self, p, L):
        """
        """
        
        y1, x1 = p
        x2, y2 = x1 + L.v[1], y1 + L.v[0]
        b, b1, b2 = [], [], []
        ps1 = [[x1 + 1,y1], [x1 - 1, y1], [x1, y1 + 1], [x1, y1 - 1]]
        ps2 = [[x2 + 1,y2], [x2 - 1, y2], [x2, y2 + 1], [x2, y2 - 1]]
        for i in range(4):
            i1, j1 = ps1[i]
            i2, j2 = ps2[i]
            if not self.out_bounds(i1, j1):
                if type(self.grid[i1][j1]) == block:
                    b1.append(self.grid[i1][j1])
            if not self.out_bounds(i2, j2):
                if type(self.grid[i2][j2]) == block:
                    b2.append(self.grid[i2][j2])

        for i in b1:
            for j in b2:
                if i == j:
                    b.append(i)
                    
        if len(b) < 1:
            return False, None
        elif len(b) == 1:
            return True, b[0]

    #function that pushes lazors until they can't
    def push_lazors(self, Ls):
        """
        """
        
        while len(Ls) != 0:
            L = Ls[0]
            y, x = L.pi
            done = False
            collision = [2,4,6]
            while not done:
                t_value, b = self.determine_block([y, x], L)
                grid_value = self.grid[x][y]
                if grid_value in collision and t_value:
                    if grid_value == 4:
                        self.grid[x][y] = 6
                    L, hit = b.lazor_interaction(L, [y, x])
                    Ls.remove(L)
                    done = True
                    for i in hit:
                        Ls.append(i)
                else:
                    if grid_value == 3:
                        self.grid[x][y] = 5
                    x, y = x + L.v[1], y + L.v[0]
                    if self.out_bounds(x, y):
                        L.pf = [y - L.v[0], x - L.v[1]]
                        done = True
                        Ls.remove(L)
            #print(L.pi, L.pf, L.v, 'final lazor')
        return self.check_win(self.grid)

    #check if game is won
    def check_win(self, grid):
        """
        """
        
        win = 0
        for row in grid:
            for value in row:
                if value == 5 or value == 6: #means lazor passes through
                    win += 1
        if win == self.goals:
            for b in self.block_list:
                print('Winner! You won!')
                print('Place Block %s on tile [%i, %i]' % (b.t, (b.p[0]-1)/2, (b.p[1]-1)/2))
            return True
        else:
            print('Loser! You are a loser!')
            return False


    #function to place block
    def block_place(self, b, p):
        """
        """
        
        y, x = b.p = p
        ps = [[x + 1,y], [x - 1, y], [x, y + 1], [x, y - 1]]
        self.grid[x][y] = b
        for x, y in ps:
            if self.grid[x][y] == 3:
                self.grid[x][y] = 4
            else:
                self.grid[x][y] = 2

    #function that solves the board
    def lazor_solver(self):
        """
        """
        
        B1, B2, B3 = self.block_list
        self.block_place(B1, [1,5])
        self.block_place(B2, [1,3])
        self.block_place(B3, [3,5])
        return self.push_lazors(self.lazor_list)

if __name__ == "__main__":
    a = lazor_game('dark_1')
    print(a.lazor_solver())
    for i in a.grid:
        print(i)