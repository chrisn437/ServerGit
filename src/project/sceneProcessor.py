import trimesh.viewer
import trimesh.scene
import trimesh
import trimesh.voxel
from trimesh.voxel.base import VoxelGrid
import trimesh.voxel.creation
import trimesh.primitives
from trimesh.exchange.binvox import voxelize_mesh
from src.Structs.Mesh import Mesh

from mpl_toolkits.mplot3d import Axes3D, art3d
import numpy as np
import matplotlib.pyplot as plt
import os


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

        self.voxelSize  : float= 0.1
        self.voxelGrid2 : VoxelGrid = trimesh.voxel.creation.local_voxelize(self.tmg, [0, 0, 0], self.voxelSize, 10)
        self.voxelGrid  : VoxelGrid = trimesh.voxel.creation.voxelize(self.tmg, self.voxelSize)

        show(self.voxelGrid.as_boxes(colors=[0.7, 0.5, 0.4, 0.4]), self.tmg)
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

            

            
            
            
                
            

    
