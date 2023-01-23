import pygame as pg
import moderngl as gl
import sys
from model import *
from camera import *
from math import *
from typing import Tuple
import physics
from mesh import *
from scene import Scene


class GameWindow:
    def __init__(self, window_size: Tuple[int, int] = (800, 600), max_fps: int = 0):
        pg.init()

        self.window_size = window_size
        self.max_fps = max_fps

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self.screen = pg.display.set_mode(self.window_size, flags=pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.glcontext = gl.create_context()
        self.glcontext.front_face = "ccw"
        self.glcontext.enable(flags=gl.DEPTH_TEST | gl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0

        self.camera = Camera(self)

        self.mesh = Mesh(self)

        self.scene = Scene(self)
        self.scene.load()

    def check_events(self, delta_time):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.release_data()
                pg.quit()
                sys.exit()

    def render(self):
        self.glcontext.clear(144 / 255, 203 / 255, 232 / 255)

        self.scene.render()

        pg.display.flip()

    def run(self):
        move_speed = 8
        sensitivity = 0.007

        while True:
            delta_time = self.clock.get_time() * 1e-3
            self.time += delta_time

            mouse_move = pg.mouse.get_rel()
            self.camera.rotate(pitch=-mouse_move[1] * sensitivity,
                               yaw=-mouse_move[0] * sensitivity)

            self.check_events(delta_time)
            pressed_keys = pg.key.get_pressed()
            if pressed_keys[pg.K_w]:
                self.camera.translate(-self.camera.forward * move_speed * delta_time)
            if pressed_keys[pg.K_s]:
                self.camera.translate(self.camera.forward * move_speed * delta_time)
            if pressed_keys[pg.K_d]:
                self.camera.translate(self.camera.right * move_speed * delta_time)
            if pressed_keys[pg.K_a]:
                self.camera.translate(-self.camera.right * move_speed * delta_time)
            if pressed_keys[pg.K_SPACE]:
                self.camera.translate(glm.vec3(0, 1, 0) * move_speed * delta_time)
            if pressed_keys[pg.K_c] or pressed_keys[pg.K_LCTRL]:
                self.camera.translate(glm.vec3(0, -1, 0) * move_speed * delta_time)

            self.render()
            pg.display.set_caption(f"Yandex3D | {int(1 / (delta_time if delta_time != 0 else 1e-6))}")
            self.clock.tick(self.max_fps)
