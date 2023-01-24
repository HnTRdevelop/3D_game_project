import glm
from math import *


FOV = 90
NEAR = 0.01
FAR = 1000.0

UP = glm.vec3(0, 1, 0)
DOWN = glm.vec3(0, -1, 0)
FORWARD = glm.vec3(0, 0, 1)
BACKWARDS = glm.vec3(0, 0, -1)
LEFT = glm.vec3(-1, 0, 0)
RIGHT = glm.vec3(1, 0, 0)


class Camera:
    def __init__(self, app):
        self.app = app
        self.aspect_ratio = app.window_size[0] / app.window_size[1]
        self.projection_matrix = self.get_projection_matrix()
        self.position = glm.vec3(0)
        self.up = UP
        self.forward = FORWARD
        self.right = RIGHT
        self.yaw = 0
        self.pitch = 0

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position - self.forward, self.up)

    def rotate(self, pitch: float = 0, yaw: float = 0):
        self.pitch += pitch
        self.yaw += yaw
        self.pitch = 90 if self.pitch > 90 else -90 if self.pitch < -90 else self.pitch
        self.forward = glm.vec3(sin(radians(self.yaw)) * cos(radians(self.pitch)),
                                -sin(radians(self.pitch)),
                                cos(radians(self.yaw)) * cos(radians(self.pitch)))
        self.forward = glm.normalize(self.forward)
        self.right = -glm.normalize(glm.cross(self.forward, UP))
        self.up = -glm.normalize(glm.cross(self.right, self.forward))

    def translate(self, translation: glm.vec3):
        self.position += translation

    def move_forward(self, move: float = 0):
        self.position -= self.forward * move

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
