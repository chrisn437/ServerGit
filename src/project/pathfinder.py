import math
import numpy as np
import pandas as pd
from collections import OrderedDict
import heapq
import matplotlib as mpl
import src.Structs.VoxelPoint as vp
from src.Structs.Vector3 import Vector3
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
#from src.project.oscNetwork import OscNetwork

# The following A* algorithm is taken from this source: https://www.analytics-link.com/post/2018/09/18/applying-the-a-path-finding-algorithm-in-python-part-3-3d-coordinate-pairs

class Pathfinder():

    def __init__(self, gridlayout, start : Vector3, end : int):
        # Creating some essential lists and setting up the start and end position
        self.x1 = []
        self.y1 = []
        self.z1 = []

        self.x2 = []
        self.y2 = []
        self.z2 = []

        self.coord_pairs = []



        self.start = start
        self.goal = end

        # Initialising the neighbors function
        self.neighbors(gridlayout)

        # Initialising the A* algorithm and gets the path (closed list) in return
        # If there is no path found self.route is set to False
        self.route = self.astar(self.start, self.goal)

        # To the path (which is a list of positions(in this case indices)) the start position gets added
        self.route = self.route + [self.start]

        # Because the route was returned from destination to the start (we added the start position in the previous step)
        # The route lsit gets now reversed so it goes from start to destination
        self.route = self.route[::-1]


    # When this function is called, it returns the calculated route
    def getRoute(self):
        return self.route

    # Setting up a list with all possible noces (points) to go to and their neighbors
    # So with the coord_pairs we define which node is a neighbor/ legal node to go to
    def neighbors(self, gridLayout):
        x1: list = []
        y1: list = []
        z1: list = []
        myIndices : list[vp.VoxelPoint] = gridLayout

        for i in myIndices:
            length = len(i.Neighbours)
            while length > 0:
                first = i.Indices3D
                if(first[0] == None):
                    pass
                if (first[1] == None):
                    pass

                x1.append(first[0])
                y1.append(first[1])
                z1.append(first[2])
                length -= 1


        x2 : list = []
        y2 : list = []
        z2 : list = []


        for i in myIndices:
            neighbours = i.Neighbours
            for y in range(len(neighbours)):
                newneighbour = neighbours[y]
                x2.append(newneighbour[0])
                y2.append(newneighbour[1])
                z2.append(newneighbour[2])



        self.coord_pairs = pd.DataFrame(OrderedDict((('x1', pd.Series(x1)), ('y1', pd.Series(y1)), ('z1', pd.Series(z1)),
                                                ('x2', pd.Series(x2)), ('y2', pd.Series(y2)), ('z2', pd.Series(z2)))))

        self.coord_pairs = self.coord_pairs.sort_values(['x1', 'y1', 'z1'], ascending=[True, True, True])

        print(self.coord_pairs)





    # Here the current position gets in, and it is looked at the available neighbors, which are defined in the coord_pairs list
    def available_neighbours(self, current_x, current_y, current_z):
        return list(zip(self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                        self.coord_pairs.z1 == current_z)][["x2"]].x2,
                        self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                                    self.coord_pairs.z1 == current_z)][["y2"]].y2,
                        self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                                    self.coord_pairs.z1 == current_z)][["z2"]].z2))

    def heuristic(self, a, b):
        # H score is calculated by this heursitic funtion. It estimates the distance to the destination
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)

    # Here the pathfinding is done. In the operation is explained in more detail
    def astar(self, start, goal):
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
        oheap = []
        heapq.heappush(oheap, (fscore[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]
            # Initializes the available neighbours function
            neighbours = self.available_neighbours(current[0], current[1], current[2])

            if current == goal:
                data = []
                while current in came_from:
                    print("Calculating path..")
                    data.append(current)
                    current = came_from[current]
                # Returns the closed list / the path from start to destination
                return data

            close_set.add(current)
            for x, y, z in neighbours:
                neighbour = x, y, z
                # Calculates the F score by adding the G score and the H score
                tentative_g_score = gscore[current] + self.heuristic(current, neighbour)

                if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                    continue

                if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                    came_from[neighbour] = current
                    gscore[neighbour] = tentative_g_score
                    fscore[neighbour] = tentative_g_score + self.heuristic(neighbour, goal)
                    heapq.heappush(oheap, (fscore[neighbour], neighbour))
        # If there is not path found return false
        return False



