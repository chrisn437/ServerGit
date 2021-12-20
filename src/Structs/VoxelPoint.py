import numpy as np
from dataclasses import dataclass
from trimesh.caching import TrackedArray
from trimesh.voxel.base import VoxelGrid
import trimesh

@dataclass
class VoxelPoint():
    """[summary]
    """
    voxelGrid : VoxelGrid = None
    """ Voxel grid from which this VoxelPoint is derived from
    """
    voxelSize : float = None
    """ Size of this voxel
    """
    transform : TrackedArray = None
    """[summary]
    """
    location : np.ndarray = None
    """ X-Y-Z position of this voxel point
    """
    Index1D : int = None
    """ Index of this point from the 1D array of voxelGrid.points
    """
    Indices3D : tuple = None
    """NP array containing neighbours in a 3D indice format 
    """
    Neighbours : np.ndarray = None