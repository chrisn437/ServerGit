import numpy as np
from dataclasses import dataclass
from trimesh.caching import TrackedArray
from trimesh.voxel.base import VoxelGrid
import trimesh

@dataclass
class VoxelPoint():
    voxelGrid : VoxelGrid = None
    voxelSize : float = None
    transform : TrackedArray = None
    location : np.ndarray = None
    Index1D : int = None
    Indices3D : tuple = None
    Neighbours : np.ndarray = None

    def visualize(self):
        origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
        
        trimesh.primitives.Box()