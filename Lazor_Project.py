
#maybe create subclasses that react to the lazor differently (option 1)
#or build in that into the block class (option 2)

class block:
    def __init__(self, position, type):
        self.p = position
        self.t = type

    #option 2
    def lazor_interaction(self,lazor):
        if self.t == 0: #opaque
            pass
        elif self.t == 1: #reflect
            pass
        elif self.t == 2: #refract
            pass


#option 1
class opaque_block(block):
    def __init__(self, position, type):
        super.__init__(self, position, type)
    
    def lazor_interaction(self,lazor):
        pass


class reflect_block(block):
    def __init__(self, position, type):
        super.__init__(self, position, type)
    
    def lazor_interaction(self,lazor):
        pass

class refract_block(block):
    def __init__(self, position, type):
        super.__init__(self, position, type)
    
    def lazor_interaction(self,lazor):
        pass



class lazor: #might not need lazor class
    def __init__(self,direction):
        self.d = direction


class grid:
    def __init__(self,board_file):
        self.board = self.read_board_file(board_file)

    def read_board_file(self, board_file):
        pass

    #creating a function that will run until it solves the lazor problem
    def lazor_solver(board_file):
        pass