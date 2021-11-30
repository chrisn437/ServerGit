import numpy as np
import src.project.sceneProcessor as sp


class Pathfinder():



    def neighbors(gridLayout):
        x1 : list = []
        y1 : list = []
        z1 : list = []
        myIndices = gridLayout

        for i in range(27):
            length = len(myIndices[i].__getattribute__('Neighbours'))
            while length > 0:
                first = myIndices[i].__getattribute__('Indices3D')
                x1.append(first[0])
                y1.append(first[1])
                z1.append(first[2])
                length -= 1
        print(x1)
        print(y1)
        print(z1)


    def available_neighbours(current_x, current_y, current_z):
        pass

    def heurisitc(a, b):
        pass

    def astar(start, goal):
        pass

    def calc_route(self):
        pass

    def get_x_and_y(self):
        pass

