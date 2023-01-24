from scene import GameObject
from components import *
from input_manager import Inputs
import pygame as pg
import glm


class Player(GameObject):
    def __init__(self, camera):
        super().__init__("Player")
        self.camera = camera

        self.move_speed = 8
        self.sensitivity = 0.007
        self.camera_height = 1.8

        self.velocity = glm.vec3(0)

    def update(self, delta_time: float):
        self.camera.rotate(pitch=-Inputs.mouse_move.y * self.sensitivity,
                           yaw=-Inputs.mouse_move.x * self.sensitivity)

        forward = glm.vec3(self.camera.forward)
        forward.y = 0
        forward = glm.normalize(forward)
        if Inputs.pressed_keys[pg.K_w]:
            self.velocity += -forward * self.move_speed
        if Inputs.pressed_keys[pg.K_s]:
            self.velocity += forward * self.move_speed
        if Inputs.pressed_keys[pg.K_d]:
            self.velocity += self.camera.right * self.move_speed
        if Inputs.pressed_keys[pg.K_a]:
            self.velocity += -self.camera.right * self.move_speed
        if Inputs.pressed_keys[pg.K_SPACE]:
            self.velocity += glm.vec3(0, 1, 0) * self.move_speed
        if Inputs.pressed_keys[pg.K_c]:
            self.velocity += glm.vec3(0, -1, 0) * self.move_speed

        self.camera.position = self.transform.position + glm.vec3(0, self.camera_height, 0)

        self.transform.translate(self.velocity * delta_time)
        self.velocity = glm.vec3(0)
