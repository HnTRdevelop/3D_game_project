import glm
from mathf import *


FOV = 90
NEAR = 0.01
FAR = 100.0


class Camera:
    def __init__(self, app):
        self.app = app
        self.aspect_ratio = app.window_size.x / app.window_size.y

        self.position = glm.vec3(2, 2, 3)
        self.up = glm.vec3(0, 1, 0)

        self.view_matrix = self.get_view_matrix()

        self.projection_matrix = self.get_projection_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, glm.vec3(0, 0, 0), self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
