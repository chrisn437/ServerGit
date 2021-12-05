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

from src.project.pathfinder import Pathfinder
from mpl_toolkits.mplot3d import Axes3D, art3d
import numpy as np
import matplotlib.pyplot as plt
import os

import src.Structs.VoxelPoint as vp

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


        self.voxelSize  : float= 0.34
        # Get the bounding box of the geometry and generate a filled voxel grid out of it
        self.bb = self.tmg.bounding_box
        self.voxelGrid : VoxelGrid = trimesh.voxel.creation.voxelize(self.bb, self.voxelSize)
        visualization = self.voxelGrid.as_boxes(colors=(1, 0.7, 0.4, 0.3)).show()

        self.voxelGrid = self.voxelGrid.fill()
        visualization = self.voxelGrid.as_boxes(colors=(1, 0.7, 0.4, 0.3)).show()


        # Create a listener position in X-Y-Z
        arr : np.ndarray = np.array([-3.124, -1.124, -2.54])

        # Retrieve a 3D coordinate (row, height, column) in which voxel the listener is located

        indices : np.ndarray = self.voxelGrid.points_to_indices(arr)


        # Use the 3D coordinate to get the voxel's index and get the centre voxel from the array new
        index = np.where(np.all(self.voxelGrid.sparse_indices == indices, axis=1))
        listenerVoxel = self.voxelGrid.points[index[0]]

        self.pointsWithNeighbours = self.getNeighbours(self.voxelGrid)
        #self.dopathfinding = Pathfinder(self.pointsWithNeighbours, start=None, end=None)


        # 1. TODO discretize the mesh
        # visualize the trimesh data

        # 2. TODO open an OSC connection and listeng for incoming messages
        # 3. TODO Calculated the shortest path using the discretized mesh and continuous position updates from the client
        # 4. TODO output the direction of navigation
        # P.s. step 3 and 4 are continuously looping

    def getMarkers(self):
        return self.tmg.metadata['markers']

    def getGrid(self):
        return self.pointsWithNeighbours

    def getNeighbours(self, vg : VoxelGrid):
        voxelSize = vg.shape
        output : list[vp.VoxelPoint] = []

        for h in range(voxelSize[0]):
            for w in range(voxelSize[1]):
                for d in range(voxelSize[2]):
                    entry = self.getNeighbour(vg, np.array([h, w, d]), voxelSize)
                    output.append(entry)
        self.testVoxelPoints(vg, output)
        return output


    def getNeighbour(self, voxelGrid : VoxelGrid, voxelIndex : np.ndarray, voxelSize : float):
        """Returns all neighbours for a given voxel indice in (X, Y, Z) format


        Args:
            voxelIndex ([type]): [description]
        """

        h = voxelIndex[0]
        w = voxelIndex[1]
        d = voxelIndex[2]
        gridSize = voxelGrid.shape

        neighbours = []
        # Brute-force for all neighbours, subtract -1 from gridsize to get 0-indexed gridSized
        if h > 0:
            neighbours.append((h - 1, w, d)) 
        if h < gridSize[0] - 1:
            neighbours.append((h + 1, w, d))
        
        if w > 0:
            neighbours.append((h, w - 1, d))
        if w < gridSize[1] - 1:
            neighbours.append((h, w + 1, d))

        if d > 0:
            neighbours.append((h, w, d - 1))
        if d < gridSize[2] - 1:
            neighbours.append((h, w, d + 1))
        
        output = vp.VoxelPoint()
        output.voxelGrid = voxelGrid
        output.voxelSize = voxelSize
        output.transform = voxelGrid.transform
        output.location = voxelGrid.indices_to_points(voxelIndex)
        output.Index1D = self.getVoxel3dTo1dIndex(voxelGrid, voxelIndex)
        output.Indices3D = voxelIndex
        output.Neighbours = np.array(neighbours)
        return output

    def testVoxelPoints(self, voxelGrid : VoxelGrid, voxelPoints : list[vp.VoxelPoint]):
        """ Ensure that voxelPoints have correctly assigned 3D and 1D indices for the corresponding location.

        Args:
            voxelGrid (VoxelGrid): Grid from which list of VoxelPoints were generated from
            voxelPoints (np.ndarray[vp.VoxelPoint]): Voxel points object generated from the voxelGrid

        Raises:
            Exception: VoxelPoint's location derived from 1D index does not match up voxelGrid
            Exception: VoxelPoint's location derived from 3D index does not match up voxelGrid
        """
        for voxPoint in voxelPoints:
            index = voxPoint.Index1D
            gridPoint = voxelGrid.points[index]
            # Test if location derived from 1D index matches the voxelGrid's 1D index location..
            if(not np.allclose(gridPoint, voxPoint.location)):
                raise Exception(f"Voxel point index {index}; value {voxPoint.location} not equal to voxelGrid. Voxelgrid value {gridPoint}")

            # Test if location derived from 3D index matches the voxelGrid's 3D index location..
            points = voxelGrid.indices_to_points(voxPoint.Indices3D)
            if(not np.allclose(points, voxPoint.location)):
                raise Exception(f"Voxel point index {index}; value {voxPoint.location} not equal to voxelGrid. Voxelgrid value {gridPoint}")
        print("Voxel Point test passed")

            


    def getVoxel3dTo1dIndex(self, voxelGrid : VoxelGrid, indices : np.ndarray):   
        """ Use the 3D coordinate to get the voxel's index and get the centre voxel from the array new
        Args:
            voxelGrid (VoxelGrid): Voxel grid
            indices (tuple): X-Y-Z indices that we wish to get the 1D array index
        """
        # Use the 3D coordinate to get the voxel's index and get the centre voxel from the array new
        index = np.where(np.all(voxelGrid.sparse_indices == indices, axis=1))[0][0]
        return index




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

            

            
            
            
                
            

    
