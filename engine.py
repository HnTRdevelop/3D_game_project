import taichi as ti


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def get_tuple(self):
        return (self.x, self.y)
        

class Vector3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def get_tuple(self):
        return (self.x, self.y, self.z)