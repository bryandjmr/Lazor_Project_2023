# Lazor_Project_2023
Repository for Group 10 in solving the Lazor Project for Software Carpentry (Fall 2023)

The way that the code works is that you define the class lazor_game with the bff file 
that you want to solve. For example, "a = lazor_game('yarn_5')". After that to get 
an output file that shows the correct placement of the blocks you need to use the
intrinsic function of the lazor_game class called lazor_solver. For example: 
"a.lazor_solver()". You should then get a text file called solutions.txt that
replicates the grid structure in the bff file format and places the blocks on the
grid so you can see where they are supposed to go. For convenience, I have written
an example code below that can be copied, along with what solutions.txt will look 
like. Have fun playing and winning!

<b>Example Code: </b>

a = lazor_game('yarn_5')
a.lazor_solver()

<b>Output of solutions.txt: </b>

Congratulations! You won! 

['o', 'B', 'x', 'o', 'o']
['o', 'A', 'o', 'o', 'o'] 
['A', 'x', 'o', 'o', 'A'] 
['o', 'x', 'A', 'o', 'x'] 
['A', 'o', 'x', 'x', 'A'] 
['B', 'A', 'x', 'A', 'o'] 

<b>Error in the Code:</b>

Our goal was to create a unique number of configurations for the placements of our blocks
in the grid. However, we greatly struggled with that so we tried to use the package
itertools.combination to create a list of all possible unordered combinations of positions.
The problem is that the code assumed all the blocks were indistinguishable, so it reduces
the number of configurations too much for levels with a high number of different types of
blocks. So the solver can handle very large grids with blocks with blocks that have limited
block diversity and can solve them quickly, but with opposite conditions, it will immediately
fail. 
