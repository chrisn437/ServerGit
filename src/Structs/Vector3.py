import numpy as np
class Vector3():
    def __init__(self, x: float, y: float, z: float) -> None:
        self.Vec3 :np.ndarray = np.array(x, y, z)