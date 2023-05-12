import pygame as pg
import moderngl as gl
import sys
from camera import Camera
from typing import Tuple
from mesh import Mesh
from scene import Scene
from input_manager import Inputs
from player import Player
from resources_loader import ResourceLoader
from static_data import StaticData


class GameWindow:
    def __init__(self, 
                 window_size: Tuple[int, int] = (800, 600), 
                 max_fps: int = 0, 
                 title: str = "GameWindow", 
                 show_fps: bool = False):
        pg.init()
        StaticData.app = self

        self.window_size = window_size
        self.max_fps = max_fps
        self.title = title
        self.show_fps = show_fps

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

        ResourceLoader.init(self.mesh)

        self.scene = Scene("BasicScene")

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
            self.scene._update(delta_time)

            self.render()
            t = self.title + (" | " + str(int(1 / (delta_time if delta_time != 0 else 1e-6))) if self.show_fps else "")
            pg.display.set_caption(t)
            self.clock.tick(self.max_fps)

    def change_scene(self, new_scene: Scene) -> Scene:
        self.scene = new_scene
        return self.scene

    def get_player(self):
        return self.player
