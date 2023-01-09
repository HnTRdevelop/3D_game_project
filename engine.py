import pygame as pg
from mathf import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Mesh:
    def __init__(self, vertices=None, triangles=None):
        self.vertices = list(vertices) if vertices is not None else list()
        self.triangles = list(triangles) if triangles is not None else list()

    def from_obj(file_path: str):
        file = open(file_path)

        verts = []
        trix = []
        for string in file.readlines():
            string = string.split()
            if string[0] == "v":
                verts.append(Vector3(float(string[1]), float(string[2]), float(string[3])))
            if string[0] == "f":
                for i in range(1, len(string)):
                    trix.extend(list(map(int, string[i].split("/"))))

        file.close()

        return Mesh(verts, trix)


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

            self.clock.tick(self.max_fps)
