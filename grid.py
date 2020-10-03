from settings import *
from node import Node

class Grid():

    def __init__(self, rows, cols, start, goal):
        
        self.row= int(rows)
        self.col = int(cols)

        self.grid = [[Node(y, x) for x in range(self.col)] for y in range(self.row)]

        self.grid[start.x][start.y] = start
        self.grid[goal.x][goal.y] = goal
        
        self.generate_all_neighbors()
    
    def generate_all_neighbors(self):

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                
                self.grid[row][col].find_neighbors(self.grid)