from math import *


class Vector3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def get_tuple(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, num: float):
        return Vector3(self.x / num, self.y / num, self.z / num)

    def __mul__(self, num: float):
        return Vector3(self.x * num, self.y * num, self.z * num)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def dist(self, other):
        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2) + pow(self.z - other.z, 2))

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


# Наследую для совместимости Vector2 и Vector3 в вычислениях
class Vector2(Vector3):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__(x, y, 0)

    def get_tuple(self):
        return self.x, self.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __truediv__(self, num: float):
        return Vector2(self.x / num, self.y / num)

    def __mul__(self, num: float):
        return Vector2(self.x * num, self.y * num)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __str__(self):
        return f"({self.x}, {self.y})"
