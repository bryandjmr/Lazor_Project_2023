"""
Lazor Project
"""

class block:
    def __init__(self, type):
        self.t = type

    #changes trajectory of lazor depending on block
    def lazor_interaction(self,lazor_beam):
        if self.t == 'A': #opaque
            return lazor()
        elif self.t == 'B': #reflect
            return lazor()
        elif self.t == 'C': #refract
            return lazor()


class lazor:
    def __init__(self, inital_p, direction):
        self.p = [int(inital_p[0]), int(inital_p[1])]
        self.v = [int(direction[0]), int(direction[1])]

    #determines if lazor reaches the goal
    def check_final(self,final): 
        return (self.v[1] / self.v[0]) == (final[1] - self.p[1]) / (final[0] - self.p[0])


class grid:
    def __init__(self,board_file):
        self.block_grid = []
        self.block_list = []
        self.lazor_list = []
        self.goal = []
        self.read_board_file(board_file)


    #reads input board file and translate it into code
    def read_board_file(self, board_file):
        if not board_file.endswith('.bff'):
            board_file += '.bff'

        read_grid = False
        with open(board_file) as board:
            for line in board:                
                if line[0] == 'G':
                    if line[5:10] == 'START':
                        read_grid = True
                    else:
                        read_grid = False
                        self.block_grid.append([0]*len(self.block_grid[0]))

                elif read_grid:
                    grid_line = line.split()
                    grid_axis = [0]*(len(grid_line)*2+1)
                    self.block_grid.append(grid_axis)
                    for i, value in enumerate(grid_line):
                        if value == 'o':
                            grid_axis[2*i+1] = 1
                    self.block_grid.append(grid_axis)

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
                    self.goal.append([int(line[2]),int(line[4])])
        board.close()

    def display(self):
        print('Grid: ', self.block_grid)
        print('Blocks: ', len(self.block_list), self.block_list)
        print('Lazors: ', len(self.lazor_list), self.lazor_list)
        print('Goals: ', len(self.goal), self.goal)

    #function that solves the board
    def lazor_solver(board_file):
        pass

if __name__ == "__main__":
    a = grid('mad_1')
    b = a.display()