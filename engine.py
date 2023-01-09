import OpenGL
import pygame as pg
from mathf import *


class GameWindow:
    def __init__(self, size: Vector2 = Vector2(800, 600), max_fps: int = 0):
        self.clock = pg.time.Clock()
        self.screen = None
        self.size = size
        self.max_fps = max_fps

    def run(self):
        self.screen = pg.display.set_mode(self.size.get_tuple())
        while True:
            delta_time = self.clock.get_time() * 1e-3

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            self.screen.fill((0, 0, 0))

            pg.display.flip()

            self.clock.tick(self.max_fps)
