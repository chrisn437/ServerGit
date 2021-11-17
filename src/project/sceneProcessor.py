import trimesh.viewer
import trimesh.scene
import trimesh
import trimesh.voxel
from trimesh.voxel.encoding import BinaryRunLengthEncoding, Encoding
import trimesh.voxel.morphology as morphology
from trimesh.voxel.base import VoxelGrid
import trimesh.voxel.creation
import trimesh.primitives
from trimesh.exchange.binvox import voxelize_mesh
from src.Structs.Mesh import Mesh

from mpl_toolkits.mplot3d import Axes3D, art3d
import numpy as np
import matplotlib.pyplot as plt
import os
import networkx as nx

def show(mesh1, mesh2=None, colors=(1, 0.7, 0.4, 0.3)):
    scene = trimesh.scene.Scene()
    scene.add_geometry(mesh1)
    if mesh2 != None:
        scene.add_geometry(mesh2)
    scene.show()


class SceneProcessor():
    """ Main brain behind quantizing the scene and calculating the navigation path
    """

    def __init__(self, trimeshgeometr:trimesh.Trimesh =None):
        self.tmg : trimesh.Trimesh = trimeshgeometr
        if self.tmg is None:
            fp = os.path.join(os.getcwd(), "permRes", "Room2.obj")
            self.tmg = trimesh.load(fp)

        self.voxelSize  : float= 0.2
    
        # Create a voxel grid
        self.voxelGrid : VoxelGrid = trimesh.voxel.creation.voxelize(self.tmg, self.voxelSize)

        # Clone and fill the voxel grid with more voxels
        self.filled : VoxelGrid = self.voxelGrid.copy().fill()
        show(self.filled.as_boxes(colors=(0.7, 0.4, 0.3, 0.3))) # visualize

        # Create a listener position in X-Y-Z
        arr : np.ndarray = np.array([0.06, 0.07, 0.04])

        # Retrieve a 3D coordinate (row, height, column) in which voxel the listener is located
        indices : np.ndarray = self.filled.points_to_indices(arr)

        # Use the 3D coordinate to get the voxel's index and get the centre voxel from the array new
        index = np.where(np.all(self.filled.sparse_indices == indices, axis=1))
        listenerVoxel = self.filled.points[index[0]]


        pass
        # 1. TODO discretize the mesh
        # visualize the trimesh data

        # 2. TODO open an OSC connection and listeng for incoming messages
        # 3. TODO Calculated the shortest path using the discretized mesh and continuous position updates from the client
        # 4. TODO output the direction of navigation
        # P.s. step 3 and 4 are continuously looping


    def extractTriangles(self, input : trimesh.Trimesh):
        counter = 0
        cubes : list[trimesh.Trimesh] = []
        vertices : np.ndarray = np.asanyarray([0.5])
        print(isinstance(vertices, np.ndarray))
     
        faces = []
        faceIndex = 0
        faceCounter = 0

        for face in input.faces:
            

            vrtx1 = input.vertices[face[0]]
            vrtxEntry = [vrtx1]
            vertices.append(vrtxEntry)

            faceEntry = []
            faceEntry.append(faceIndex)
            faceIndex += 1
            faceEntry.append(faceIndex)
            faceIndex += 1
            faceEntry.append(faceIndex)
            faceIndex += 1

            faces.append(faceEntry)

            faceCounter += 1

            if(faceCounter % 8 == 0):
                entry = trimesh.Trimesh(vertices, faces)
                cubes.append(entry)
                vertices.clear()
                faces.clear()
                faceCounter = 0

            

            
            
            
                
            

    
