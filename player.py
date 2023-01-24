from scene import GameObject
from components import *
from input_manager import Inputs
import pygame as pg
import glm


class Player(GameObject):
    def __init__(self, camera):
        super().__init__("Player")
        self.camera = camera

        self.max_speed_ground = 320 / 37.65
        self.max_speed_air = 30 / 37.65
        self.max_accel = 10 * self.max_speed_ground
        self.sensitivity = 0.007
        self.camera_height = 1.8

        self.gravity = -9.81

        self.velocity = glm.vec3(0)

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

        if self.transform.position.y < 0:
            self.transform.position.y = 0
            self.velocity.y = 0

        if Inputs.pressed_keys[pg.K_SPACE] and self.transform.position.y == 0:
            self.velocity.y = 4

        if self.transform.position.y == 0:
            self.update_velocity_ground(wishdir, delta_time)
        else:
            self.update_velocity_air(wishdir, delta_time)
            self.velocity += up * self.gravity * delta_time

        self.transform.translate(self.velocity * delta_time)
        self.camera.position = self.transform.position + glm.vec3(0, self.camera_height, 0)

    def update_velocity_ground(self, wishdir: glm.vec3, delta_time: float):
        self.friction(delta_time)

        current_speed = glm.dot(self.velocity, wishdir)
        add_speed = glm.clamp(self.max_speed_ground - current_speed, 0, self.max_accel * delta_time)

        self.velocity += add_speed * wishdir

    def update_velocity_air(self, wishdir: glm.vec3, delta_time: float):
        current_speed = glm.dot(self.velocity, wishdir)
        add_speed = glm.clamp(self.max_speed_ground - current_speed, 0, self.max_accel * delta_time)

        self.velocity += add_speed * wishdir

    def friction(self, delta_time: float):
        self.velocity -= self.velocity * delta_time * 10
