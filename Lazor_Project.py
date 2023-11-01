
#maybe create subclasses that react to the lazor differently 
#or build in that into the block class

class block:
    def __init__(self, position, type):
        self.p = position
        self.t = type



class lazor:
    def __init__(self,direction):
        self.d = direction


#creating a function that will run until it solves the lazor problem
def lazor_solver(board_file):
    pass