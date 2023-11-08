"""
Lazor Project
"""

class block:
    def __init__(self, position, type):
        self.p = position
        self.t = type

    #changes trajectory of lazor depending on block
    def lazor_interaction(self,lazor_beam):
        if self.t == 0: #opaque
            return lazor()
        elif self.t == 1: #reflect
            return lazor()
        elif self.t == 2: #refract
            return lazor()


class lazor:
    def __init__(self, inital_p, direction):
        self.p = inital_p
        self.v = direction

    #determines if lazor reaches the goal
    def check_final(self,final): 
        return (self.v[1] / self.v[0]) == (final[1] - self.p[1]) / (final[0] - self.p[0])


class grid:
    def __init__(self,board_file):
        self.board = self.read_board_file(board_file)

    #reads input board file and translate it into code
    def read_board_file(self, board_file):
        pass

    #function that solves the board
    def lazor_solver(board_file):
        pass