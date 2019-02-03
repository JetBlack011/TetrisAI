# TetrisAI
A simple NES Tetris AI for emulators. Just as a preface, no, this project is not finished, and I'm not sure if it will be for quite a while. However, I felt the need to keep this posted regardless, because it is representative of my first real attempt at writing any type of AI which plays a game based off of screen interpretation, and it truly was a project from which I learned a great deal.

# The Basic Idea
This entire repository was initiated with motivation derived from [here](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/), Yiyuan Lee's implementation of a "perfect" Tetris AI. Also, I would be lying if I claimed [CodeBullet](https://www.youtube.com/channel/UC0e3QhIYukixgh5VVpKHH9Q) and his awesome projects involving game AIs didn't influence my project choice. Regardless, the algorithm itself was implemented based upon Lee's project, so full credit goes to him. Very simply, my version of this AI functions using the summation of 4 heuristic variables of the game state -- aggregated height, complete lines, holes, and bumpiness -- retrieved through OpenCV templating and grid simulation. This simulation is completed using a 10x22 (classic tetris dimensions) numpy array, where within a "0" represents an empty space and a "1" represents a space occupied by a Mino. For example: 
```[[0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 1. 1. 0. 0. 0. 0.]
 [1. 1. 1. 1. 1. 1. 0. 0. 0. 0.]
 [1. 1. 1. 1. 1. 1. 0. 0. 0. 0.]
 [1. 1. 1. 1. 1. 1. 0. 0. 0. 0.]
 [0. 1. 1. 1. 1. 1. 0. 0. 0. 0.]]
Current Piece: I, Next Piece: T
Best Origin: 0, Best Rotation: 1
```
The method for completing a simulated drop works by calculating the distance from the lowest occupied space in a predefined constant ndarray of the Tetromino to the tallest column, then overlaying the two matrices, preserving the already-occupied spaces on the grid.
```
[[1, 1, 1],
[0, 1, 0]]
```
This was likely the most difficult to implement portion of this project and is, somewhat ironically, the only portion that functions correctly consistently. The "scoring" function, used to determine the optimal move based off of the current game state, loops through each possible origin and rotation for the current Tetromino and calculates its respective score using the simulation, which, afterwards, has its state reverted to the optimal drop. From a retrospective paradigm, everything should function fairly smoothly, however, the main issue resides in both the algorithm itself and the movement algorithm.

# Current Status
At the moment, this project contains a practically nonfunctional AI that tries to fling pieces based off of a faultily implemented algorithm. It has numerous compatibility issues, only interacting with games hosted on a particular resolution. Moreover, the keyboard interaction is completed through interaction with the winapi (due to malfunction whilst running with my current emulator setup), and greatly restricts the usage of this script on anything more than a *very* specfic environment.

# TODOs
Should I ever regain motivation to continue this program, which may come with time and lack of ulterior, more alluring projects, there would be plenty of work to be done perfecting the simulation functionality, keyboard interaction, etc. 
