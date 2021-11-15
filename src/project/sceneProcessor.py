import trimesh.viewer
import trimesh.scene
import trimesh
import trimesh.voxel
import trimesh.voxel.creation
import trimesh.primitives
from trimesh.exchange.binvox import voxelize_mesh
from src.Structs.Mesh import Mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d


def show(chair_mesh, chair_voxels, colors=(1, 1, 1, 0.3)):
    scene = chair_mesh.scene()
    scene.add_geometry(chair_voxels.as_boxes(colors=colors))
    scene.show()


class SceneProcessor():
    """ Main brain behind quantizing the scene and calculating the navigation path
    """

    def __init__(self, trimeshgeometry):
        self.trimeshgeometry = trimeshgeometry
        self.voxelSize = 0.34
        self.voxelGrid : trimesh.voxel.VoxelGrid = trimesh.voxel.creation.voxelize(self.trimeshgeometry, self.voxelSize)
        isFilled =self.voxelGrid.is_filled([0, 0, 0])
        geo = self.voxelGrid.as_boxes(colors=(0.7, 0.5, 0.1, 0.25))



        points = self.voxelGrid.points
        for p in points:
            b = trimesh.primitives.Box
            b.apply_scale(self.voxelSize)
            o = self.voxelGrid.indices_to_points(p)
            print(o)





        print("Scene processor initialized")
        print(self.voxelGrid.filled_count)
        newScene = trimesh.scene.Scene()
        newScene.add_geometry(geo)
        newScene.add_geometry(self.trimeshgeometry)
        
        self.extractTriangles(geo)

        newScene.show()

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
        vertices : np.ndarray = []
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

            

            
            
            
                
            

    
