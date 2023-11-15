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

Example Code:
a = lazor_game('yarn_5')
a.lazor_solver()

Output of solutions.txt:

Congratulations! You won! 

['o', 'B', 'x', 'o', 'o']
['o', 'A', 'o', 'o', 'o'] 
['A', 'x', 'o', 'o', 'A'] 
['o', 'x', 'A', 'o', 'x'] 
['A', 'o', 'x', 'x', 'A'] 
['B', 'A', 'x', 'A', 'o'] 
