from scene import GameObject
from components import *
from input_manager import Inputs
import pygame as pg
import glm


class Player(GameObject):
    def __init__(self, camera):
        super().__init__("Player")
        self.camera = camera

        self.move_speed = 5
        self.sensitivity = 0.03
        self.camera_height = 0.0

    def update(self, delta_time: float):
        self.camera.rotate(pitch=Inputs.mouse_move.y * self.sensitivity,
                           yaw=-Inputs.mouse_move.x * self.sensitivity)

        forward = glm.vec3(self.camera.forward)
        forward.y = 0
        forward = glm.normalize(forward)
        right = self.camera.right
        up = glm.vec3(0, 1, 0)

        wishdir = forward * Inputs.pressed_keys[pg.K_w] - forward * Inputs.pressed_keys[pg.K_s]
        wishdir += right * Inputs.pressed_keys[pg.K_d] - right * Inputs.pressed_keys[pg.K_a]
        wishdir += up * Inputs.pressed_keys[pg.K_e] - up * Inputs.pressed_keys[pg.K_q]

        self.transform.translate(wishdir * self.move_speed * delta_time)
        self.camera.position = self.transform.position + glm.vec3(0, self.camera_height, 0)
