from settings import *

class Node():
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y

        self.type = 0 # 0=Empty

        self.f = 0
        self.g = 0
        self.h = 0

        self.neighbors = []
        self.parent = None
        
    def find_neighbors(self, grid):
        x = self.x
        y = self.y

        self.neighbors = []
        
        if (x < (HEIGHT/TILESIZE) - 1):
            self.neighbors.append(grid[x+1][y])
        if (x > 0):
            self.neighbors.append(grid[x-1][y])
        if (y < (WIDTH/TILESIZE) - 1):
            self.neighbors.append(grid[x][y+1])
        if (y > 0):
            self.neighbors.append(grid[x][y-1])

        
    def h(self, goal_x, goal_y):
        dx = abs()