import pygame
import random
import math

from settings import *
from grid import Grid
from node import Node

class Game:

    def __init__(self):

        pygame.init()
        self.h_weight = 1
        self.g_weight = 1
        
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.mouse_position = [0,0]

        self.placement_type = 3 # 1=Start, 2=Goal, 3=Wall, 0=Empty
        self.runsim = False


        
        self.starting_tile = Node(0,0); self.starting_tile.type = 1
        self.goal_tile = Node(20,10); self.goal_tile.type = 2#Node(int((HEIGHT/TILESIZE) - 1), int((WIDTH/TILESIZE) - 1)); self.goal_tile.type = 2
        self.grid = Grid( (HEIGHT/TILESIZE), (WIDTH/TILESIZE), self.starting_tile, self.goal_tile )

        self.visitedNodes = []
        self.openNodes = [self.starting_tile]
        self.finalPath = []




    def new(self):

        print("Controls: ")
        print("1: Cycle through placements")
        print("2: Reset Grid")
        print("3: Reset Walls")

        self.run()
    
    def run(self):

        self.playing = True
        
        while (self.playing):
            
            #self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

            if (self.runsim):

                if (len(self.openNodes) > 0):
                    
                    best_cost_index = 0
                    for i in range(len(self.openNodes)):
                        if (self.openNodes[i].f < self.openNodes[best_cost_index].f): # TODO .f might need to be .getF
                            best_cost_index = i

                    currentNode = self.openNodes[best_cost_index]

                    if ((self.openNodes[i].x == self.goal_tile.x) and (self.openNodes[i].y == self.goal_tile.y)):
                        
                        lastNode = self.openNodes[i]
                        self.finalPath.append(lastNode)
                        
                        while ( lastNode.parent != None ):
                            self.finalPath.append(lastNode.parent)
                            lastNode = lastNode.parent

                        print("Path found!")
                        self.runsim = False
                        continue

                    self.openNodes.remove(currentNode)
                    self.visitedNodes.append(currentNode)

                    for neighbor in currentNode.neighbors:
                        
                        if (neighbor.type != 3):
                            if (neighbor not in self.visitedNodes):
                                tentative_GScore = (currentNode.g + 1) * self.g_weight #self.euclidian_distance(neighbor, self.goal_tile) 

                                if (neighbor in self.openNodes):
                                    if (tentative_GScore < neighbor.g):
                                        neighbor.g = tentative_GScore
                                else:
                                    neighbor.g = tentative_GScore
                                    self.openNodes.append(neighbor)

                                neighbor.h = self.manhattan_heuristic(neighbor, self.goal_tile)
                                neighbor.f = neighbor.g + neighbor.h
                                neighbor.parent = currentNode

                else:

                    print("No possible path")
                    self.runsim = False
            else:

                for row in range(len(self.grid.grid)):
                    for col in range(len(self.grid.grid[row])):
                        
                        if (self.grid.grid[row][col].type not in (1,2,3)):
                            self.grid.grid[row][col].type = 0
                

    def update(self):

        self.mouse_position = pygame.mouse.get_pos()

    def events(self):
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if (self.playing):
                    self.playing = False
                self.running = False
            if pygame.mouse.get_pressed()[0]:
                x_col = pygame.mouse.get_pos()[0]
                y_row = pygame.mouse.get_pos()[1]

                clicked_col = int(x_col/TILESIZE)
                clicked_row = int(y_row/TILESIZE)

                #print("Tile: " + str( clicked_row ), str( clicked_col ))

                self.grid.grid[clicked_row][clicked_col].type = self.placement_type 

                if (self.placement_type == 1):
                    self.grid.grid[self.starting_tile.x][self.starting_tile.y].type = 0
                    self.starting_tile.x = clicked_row; self.starting_tile.y = clicked_col
                    self.grid.grid[clicked_row][clicked_col] = self.starting_tile
                    self.grid.generate_all_neighbors()
                    self.openNodes = [self.starting_tile]
                if (self.placement_type == 2):

                    self.grid.grid[self.goal_tile.x][self.goal_tile.y].type = 0
                    self.grid.grid[clicked_row][clicked_col].type = 2
                    self.goal = self.grid.grid[clicked_row][clicked_col]

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.runsim = not self.runsim

                if event.key == pygame.K_1:
                    self.placement_type += 1

                    if self.placement_type >= 4:
                        self.placement_type = 1

                    if (self.placement_type == 1):
                        print("Placing START")
                    elif (self.placement_type == 2):
                        print("Placing GOAL")
                    elif (self.placement_type == 3):
                        print("Placing WALL")


                if event.key == pygame.K_2:
                    self.visitedNodes = []
                    self.openNodes = [self.starting_tile]
                    self.finalPath = []
                    self.runsim = False
                    print("Grid reset!")
                
    def draw(self):

        self.screen.fill(WHITE)

        # Draw lists of nodes
        for node in self.visitedNodes:
             pygame.draw.rect(self.screen, LIGHT_RED, ((node.y*TILESIZE, node.x*TILESIZE), (TILESIZE, TILESIZE)))
        for node in self.openNodes:
            pygame.draw.rect(self.screen, LIGHT_GREEN, ((node.y*TILESIZE, node.x*TILESIZE), (TILESIZE, TILESIZE)))

        # Draw start and goal tile
        pygame.draw.rect(self.screen, GREEN, ((self.starting_tile.y*TILESIZE, self.starting_tile.x*TILESIZE), (TILESIZE, TILESIZE)))
        pygame.draw.rect(self.screen, BLUE, ((self.goal_tile.y*TILESIZE, self.goal_tile.x*TILESIZE), (TILESIZE, TILESIZE)))

        # Draw all the walls
        for row in range( len(self.grid.grid) ):
            for col in range( len(self.grid.grid[row]) ):
                
                coords = self.grid.grid[row][col].type
                if (coords == 3):
                    pygame.draw.rect(self.screen, GRAY, ((col*TILESIZE, row*TILESIZE), (TILESIZE, TILESIZE)))

        # Draw final path
        if (self.finalPath != []):
            for node in self.finalPath:
                pygame.draw.rect(self.screen, YELLOW, ((node.y*TILESIZE, node.x*TILESIZE), (TILESIZE, TILESIZE)))

        # Draw grid lines here
        # Usings lines instead of drawing full tiles is more efficient
        for y in range(int(HEIGHT/TILESIZE)):
            pygame.draw.line(self.screen, BLACK, [0, y*TILESIZE], [WIDTH, y*TILESIZE], 1)
        for x in range(int(WIDTH/TILESIZE)):
            pygame.draw.line(self.screen, BLACK, [x*TILESIZE, 0], [x*TILESIZE, HEIGHT], 1)

        pygame.display.flip()

    def euclidian_distance(self, a, b):
        distance = math.hypot((a.x - a.y), (b.x -b.y)) * self.h_weight
        return distance
    
    def manhattan_heuristic(self, a, b):
        weight = self.h_weight

        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)

        return weight * (dx + dy)


if __name__ == "__main__":

    g = Game()
    g.run()

    while (g.running):
        pass
    pygame.quit()
