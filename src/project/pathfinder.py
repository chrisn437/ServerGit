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

class Pathfinder():

    def __init__(self, gridlayout, start : Vector3, end : int):
        self.x1 = []
        self.y1 = []
        self.z1 = []

        self.x2 = []
        self.y2 = []
        self.z2 = []

        self.coord_pairs = []



        self.start = start
        self.goal = end

        self.neighbors(gridlayout)


        self.route = self.astar(self.start, self.goal)

        self.route = self.route + [self.start]

        self.route = self.route[::-1]

        #print(self.route)

        self.x_coords: list = []

        self.y_coords: list = []

        self.z_coords: list = []

        for i in (range(0, len(self.route))):
            x = self.route[i][0]

            y = self.route[i][1]

            z = self.route[i][2]

            self.x_coords.append(x)

            self.y_coords.append(y)

            self.z_coords.append(z)

        self.x_coords = np.array(self.x_coords)

        self.y_coords = np.array(self.y_coords)

        self.z_coords = np.array(self.z_coords)

        #self.defangel(self.route)

    def getRoute(self):
        return self.route

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
        #print(x1)
        #print(y1)
        #print(z1)

        #print(len(x1))
        #print(len(y1))
        #print(len(z1))

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






    def available_neighbours(self, current_x, current_y, current_z):
        return list(zip(self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                        self.coord_pairs.z1 == current_z)][["x2"]].x2,
                        self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                                    self.coord_pairs.z1 == current_z)][["y2"]].y2,
                        self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                                    self.coord_pairs.z1 == current_z)][["z2"]].z2))

    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)

    def astar(self, start, goal):
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
        oheap = []
        heapq.heappush(oheap, (fscore[start], start))
        iter: int = 0

        while oheap:
            #print(f"oheap iter {iter}")
            iter += 1
            current = heapq.heappop(oheap)[1]
            neighbours = self.available_neighbours(current[0], current[1], current[2])

            if current == goal:
                data = []
                while current in came_from:
                    print("Calculating path..")
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)
            for x, y, z in neighbours:
                neighbour = x, y, z
                tentative_g_score = gscore[current] + self.heuristic(current, neighbour)

                if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                    continue

                if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                    came_from[neighbour] = current
                    gscore[neighbour] = tentative_g_score
                    fscore[neighbour] = tentative_g_score + self.heuristic(neighbour, goal)
                    heapq.heappush(oheap, (fscore[neighbour], neighbour))

        return False



