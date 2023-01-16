import pygame as pg
import moderngl as gl
import sys
from mathf import *
from model import *
from camera import *


class GameWindow:
    def __init__(self, window_size: Vector2 = Vector2(800, 600), max_fps: int = 0):
        pg.init()

        self.window_size = window_size
        self.max_fps = max_fps

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.window_size.get_tuple(), flags=pg.OPENGL | pg.DOUBLEBUF)

        self.glcontext = gl.create_context()

        self.clock = pg.time.Clock()
        self.time = 0

        self.camera = Camera(self)

        self.scene = Mesh(self)

    def check_events(self, delta_time):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.release_data()
                pg.quit()
                sys.exit()

    def render(self):
        self.glcontext.clear(0.2, 0.2, 0.2)

        self.scene.render()

        pg.display.flip()

    def run(self):
        while True:
            delta_time = self.clock.get_time() * 1e-3
            self.time += delta_time

            self.check_events(delta_time)

            self.render()
            pg.display.set_caption(f"Yandex3D | {1 / (delta_time if delta_time != 0 else 1e-6)}")
            self.clock.tick(self.max_fps)
