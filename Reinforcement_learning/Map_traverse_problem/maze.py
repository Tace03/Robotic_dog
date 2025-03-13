
import numpy as np
import sys
import random
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0,1)
DOWN = (0, -1)

FINISH_P = 1
PATH_P = 0
WALL_P = -1


class MazeMaker:
    def __init__(self
                 , x 
                 , y ):
        self.x = x + 2
        self.y = y + 2

        self.maze = np.empty(shape= (self.x, self.y))
        self.maze.fill(WALL_P)

        self.path_list = [(1,1)]
        self.frontier_list = [(1,1)]
        self.generateMaze()
        self.writeMazeToText()
    
    def printMaze(self):
        print(np.transpose(self.maze))
    
    def generateMaze(self):
        self.maze[1][1] = PATH_P
        
        while(len(self.frontier_list) > 0):
            # take one cell from the frontier
            frontier_cell = random.choice(self.frontier_list)
            # print("Now processing : ", frontier_cell)

            # assess expandibility of the cell
            #expand = self.is_expandible(frontier_cell)

            # expand the maze
            
            self.expand_cell(frontier_cell)

    def expand_cell(self, cell):
        temp_move = []
        direction_choice = [0, 1, 2, 3]
        while(1):
            if len(direction_choice) == 0:
                if(cell in self.frontier_list):
                    self.frontier_list.remove(cell)
                break
            random_direction = random.choice(direction_choice)
            temp_move.append(random_direction)
            direction_choice.remove(random_direction)

            if random_direction == 0:
                temp_coordinate = (cell[0] + 1, cell[1])
            elif random_direction == 1:
                temp_coordinate = (cell[0], cell[1] + 1)
            elif random_direction == 2:
                temp_coordinate = (cell[0] - 1, cell[1])
            elif random_direction == 3:
                temp_coordinate = (cell[0], cell[1] - 1)

            if(self.expand_direction(temp_coordinate, cell)):
                break
        
                

    def expand_direction(self, test_cell, parent_cell):
        # checking if the coordinate is valid
        if self.isCoordinate(test_cell[0], test_cell[1]) == False:
            return False
        
        # print("Trying to expand cell: ", test_cell)

        # if the cell is valid
        if ((test_cell[0], test_cell[1]) not in self.path_list):
            # check if it is valid to put in this space (as in 4 nearest cell is not a path already)
            expand = self.is_expandible(test_cell, parent_cell)

            # If the cell cannot be a path, deny it
            if(not expand):
                return False

            self.maze[test_cell[0]][test_cell[1]] = PATH_P
            self.path_list.append(test_cell)
            self.frontier_list.append(test_cell)

            # sanitize check if parent is still a frontier cell
            expand = self.is_frontier(parent_cell)

            if(not expand):
                if(parent_cell in self.frontier_list):
                    self.frontier_list.remove(parent_cell)

            # print("Path list includes: ", len(self.path_list))
            # print(self.path_list)
            # print(self.maze)

            return True
        else:
            return False

    def is_frontier(self, test_cell):
        count = 0
        if(self.isCoordinate(test_cell[0] + 1, test_cell[1])):
            if(self.maze[test_cell[0] + 1][test_cell[1]] == PATH_P):
                count += 1
        else:
            count += 1
                
        if(self.isCoordinate(test_cell[0], test_cell[1] + 1)):
            if(self.maze[test_cell[0]][test_cell[1] + 1] == PATH_P):
                count += 1
        else:
            count += 1
        
        if(self.isCoordinate(test_cell[0] - 1, test_cell[1])):
            if(self.maze[test_cell[0] - 1][test_cell[1]] == PATH_P):
                count += 1
        else:
            count += 1
                
        if(self.isCoordinate(test_cell[0], test_cell[1] - 1)):
            if(self.maze[test_cell[0]][test_cell[1] - 1] == PATH_P):
                count += 1
        else:
            count += 1
        if count != 4:
            return True
        else:
            return False

    def is_expandible(self, test_cell, parent_cell) -> bool: 
        if(self.isCoordinate(test_cell[0] + 1, test_cell[1])):
            if(self.maze[test_cell[0] + 1][test_cell[1]] == PATH_P):
                if(test_cell[0] + 1, test_cell[1]) != parent_cell:
                    return False
                
        if(self.isCoordinate(test_cell[0], test_cell[1] + 1)):
            if(self.maze[test_cell[0]][test_cell[1] + 1] == PATH_P):
                if(test_cell[0], test_cell[1] + 1) != parent_cell:
                    return False
        
        if(self.isCoordinate(test_cell[0] - 1, test_cell[1])):
            if(self.maze[test_cell[0] - 1][test_cell[1]] == PATH_P):
                if(test_cell[0] - 1, test_cell[1]) != parent_cell:
                    return False
                
        if(self.isCoordinate(test_cell[0], test_cell[1] - 1)):
            if(self.maze[test_cell[0]][test_cell[1] - 1] == PATH_P):
                if(test_cell[0], test_cell[1] - 1) != parent_cell:
                    return False
        
            
        return True


    def isCoordinate(self, coor_x, coor_y) -> bool: 
        if(coor_x <= 0 or coor_x >= self.x - 1):
            return False
        if(coor_y <= 0 or coor_y >= self.y - 1):
            return False
        return True
    
    def writeMazeToText(self):
        maze_text = ""
        for x in range(self.maze.shape[0]):
            for y in range(self.maze.shape[1]):
                if self.maze[x][y] == WALL_P:
                    maze_text += '*'
                elif self.maze[x][y] == PATH_P:
                    maze_text += ' '
                else:
                    maze_text += '1'
            maze_text += '\n\n'
        #print(maze_text)
        maze_file =  open('maze.txt', 'w')
        maze_file.write(maze_text)
        maze_file.close()
    
    def visualize(self):
        """Visualizes the maze using Matplotlib."""
        maze_display = self.maze.copy()
        maze_display[0, 0] = 2  # Mark agent position with a special value

        # Define colors: 0 = Free path, -1 = Wall, 1 = Goal, 2 = Agent
        colors = {0: 'white', -1: 'black', 1: 'green', 2: 'red'}
        cmap = [[colors[val] for val in row] for row in maze_display]

        fig, ax = plt.subplots()
        ax.imshow(maze_display, cmap='coolwarm', vmin=-1, vmax=2)

        # Grid lines for better visibility
        ax.set_xticks(np.arange(-0.5, maze_display.shape[1], 1), minor=True)
        ax.set_yticks(np.arange(-0.5, maze_display.shape[0], 1), minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
        ax.tick_params(which="both", size=0, labelbottom=False, labelleft=False)

        plt.show()


maze1 = MazeMaker(20,30)

maze1.visualize()