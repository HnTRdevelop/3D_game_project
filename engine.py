import pygame as pg
import moderngl as gl
import sys
from camera import Camera
from math import *
from typing import Tuple
import physics
from mesh import Mesh
from scene import Scene
from resources_loader import load_resources
import glm
from input_manager import Inputs
from player import Player


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
        self.player = Player(self.camera)

        self.mesh = Mesh(self)
        load_resources(self.mesh)

        self.scene = Scene(self, self.player)

    def check_events(self, delta_time: float):
        Inputs.get_inputs()
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
        while True:
            delta_time = self.clock.get_time() * 1e-3
            self.time += delta_time

            self.check_events(delta_time)
            self.scene.update(delta_time)

            self.render()
            pg.display.set_caption(f"Yandex3D | {int(1 / (delta_time if delta_time != 0 else 1e-6))}")
            self.clock.tick(self.max_fps)
