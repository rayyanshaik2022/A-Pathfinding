# A* Pathfinding
- This project demonstrates the usage of the A* (A star) pathfinding algorithm on a 2d grid.
- The pathfinding algorithm in this situation searches from a singular start point, to a singular end/goal point

## Dependencies
- pygame
  - Used to draw the grid and display the graphics

## Development challenges
- This project was created when I first learned about Object Oriented Programming (OOP). At first I had struggles defining what a "node" would be, and how to efficiently use node. In the end, I was able to create a node class which was then used to represent every cell on the board
- Processing limitations and efficiency
  - Due to the nature of the algorithm, the more open nodes there are, the less efficient the code runs (causing the program to run slower). Paired with the fact that python + a drawing library is not especially fast, I had challenges with making this program usable. The solution I found was to be very meticulous with how I was iterating over loops - don't do it more than necessary and do it effectively. 

## Usage:
- Number Key 1: Cycles through placing the start location, goal location, and walls
- Number Key 2: Clears all walls
- Space Bar: Runs the pathfinding algorithm
