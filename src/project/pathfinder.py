import numpy as np
import pandas as pd
from collections import OrderedDict
import heapq
import src.Structs.VoxelPoint as vp
from src.Structs.Vector3 import Vector3
"""Originally taken from https://www.analytics-link.com/post/2018/09/18/applying-the-a-path-finding-algorithm-in-python-part-3-3d-coordinate-pairs

Modifications by Christian Neurhor`"""

class Pathfinder():
    """Pathfinder, takes in the start-, end- position, and the list of voxel points"""
    def __init__(self, gridlayout, start : Vector3, end : int):
        # creating a list to save information
        self.coord_pairs = []
        # setting start and end indicie to variable
        self.start = start
        self.goal = end

        # taking the voixel points and their neighbours
        self.neighbors(gridlayout)

        # getting the route indices, but it is in reverse (from end to start)
        self.route = self.astar(self.start, self.goal)
        # adding the start position indice to the route list
        self.route = self.route + [self.start]
        # reversing to route list
        self.route = self.route[::-1]


    def getRoute(self):
        # when this function is called, it returns the route
        return self.route

    def neighbors(self, gridLayout):
        # taking in all the voxel points and their neighbours and saving it to lists
        x1: list = []
        y1: list = []
        z1: list = []
        # saving all voxel points
        myIndices : list[vp.VoxelPoint] = gridLayout
        for i in myIndices:
            length = len(i.Neighbours)
            while length > 0:
                first = i.Indices3D
                x1.append(first[0])
                y1.append(first[1])
                z1.append(first[2])
                length -= 1

        x2 : list = []
        y2 : list = []
        z2 : list = []
        # saving all the available neighbours
        for i in myIndices:
            neighbours = i.Neighbours
            for y in range(len(neighbours)):
                newneighbour = neighbours[y]
                x2.append(newneighbour[0])
                y2.append(newneighbour[1])
                z2.append(newneighbour[2])


        # defining all the possible neighbours of all voxelpoints
        self.coord_pairs = pd.DataFrame(OrderedDict((('x1', pd.Series(x1)), ('y1', pd.Series(y1)), ('z1', pd.Series(z1)),
                                                ('x2', pd.Series(x2)), ('y2', pd.Series(y2)), ('z2', pd.Series(z2)))))
        self.coord_pairs = self.coord_pairs.sort_values(['x1', 'y1', 'z1'], ascending=[True, True, True])


    def available_neighbours(self, current_x, current_y, current_z):
        # returns all neighbours from the current voxelpoint
        return list(zip(self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                        self.coord_pairs.z1 == current_z)][["x2"]].x2,
                        self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                                    self.coord_pairs.z1 == current_z)][["y2"]].y2,
                        self.coord_pairs.loc[(self.coord_pairs.x1 == current_x) & (self.coord_pairs.y1 == current_y) & (
                                    self.coord_pairs.z1 == current_z)][["z2"]].z2))

    def heuristic(self, a, b):
        # calculating the H score
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)

    def astar(self, start, goal):
        """the pathfinding is inizialized here"""
        # prevents dublicates
        close_set = set()
        # creating the closed list
        came_from = {}
        # setting the G score at the beginning
        gscore = {start: 0}
        # setting the F score at the beginning
        fscore = {start: self.heuristic(start, goal)}
        # creating the open list
        oheap = []
        heapq.heappush(oheap, (fscore[start], start))


        while oheap:
            # setting the startpoint the the current position
            current = heapq.heappop(oheap)[1]
            # saving all the available neighbours in that variable
            neighbours = self.available_neighbours(current[0], current[1], current[2])

            # if the algorithm found the destination return the parent list
            if current == goal:
                data = []
                while current in came_from:
                    print("Calculating path..")
                    data.append(current)
                    current = came_from[current]
                return data

            # adding the current position to the closed list and checking if it is already in it
            close_set.add(current)
            for x, y, z in neighbours:
                neighbour = x, y, z
                # checking the tentative G score for all available neighbors
                tentative_g_score = gscore[current] + self.heuristic(current, neighbour)

                # checking if one of the neighbours is in the closed list and has a higher G score, if so then continue
                if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                    continue

                # if the G score is lower, or the neighbour is not int the open list already
                if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                    # then add that voxel point to the closed set and save that G and F score
                    came_from[neighbour] = current
                    gscore[neighbour] = tentative_g_score
                    fscore[neighbour] = tentative_g_score + self.heuristic(neighbour, goal)
                    heapq.heappush(oheap, (fscore[neighbour], neighbour))

        # if no path is found, return false
        return False
