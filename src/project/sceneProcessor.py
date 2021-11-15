import trimesh.viewer
import trimesh.scene
from src.Structs.Mesh import Mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d


class SceneProcessor():
    """ Main brain behind quantizing the scene and calculating the navigation path
    """

    def __init__(self, trimeshgeometry):
        self.trimeshgeometry = trimeshgeometry
        self.trimeshscene = trimesh.scene.Scene(geometry=self.trimeshgeometry)
        trimesh.viewer.SceneViewer(scene=self.trimeshscene)
        print("Scene processor initialized")
        # 1. TODO discretize the mesh
        # visualize the trimesh data


        # 2. TODO open an OSC connection and listeng for incoming messages
        # 3. TODO Calculated the shortest path using the discretized mesh and continuous position updates from the client
        # 4. TODO output the direction of navigation
        # P.s. step 3 and 4 are continuously looping
