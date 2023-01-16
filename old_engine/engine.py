import pygame as pg
from pygame.locals import *
from mathf import *
from OpenGL.GL import *
from OpenGL.GLU import *


pg.init()
COLORS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1)]


class Mesh:
    def __init__(self, vertices=None, triangles=None, edges=None):
        self.vertices = list(vertices) if vertices is not None else list()
        self.triangles = list(triangles) if triangles is not None else list()
        self.edges = list(edges) if edges is not None else list()

    def load_to_opengl_wire(self, offset: Vector3 = Vector3()):
        glBegin(GL_LINES)
        for edge in self.edges:
            glVertex3fv((self.vertices[edge - 1] - offset).get_tuple())
        glEnd()

    def load_to_opengl_faces(self, offset: Vector3 = Vector3()):
        glBegin(GL_TRIANGLES)
        for tris in self.triangles:
            glVertex3fv((self.vertices[tris - 1] - offset).get_tuple())
        glEnd()


def from_obj(file_path: str) -> Mesh:
    file = open(file_path)

    verts = []
    trix = []
    edges = []
    for string in file.readlines():
        string = string.split()
        if len(string) == 0:
            continue
        if string[0] == "v":
            verts.append(Vector3(float(string[1]), float(string[2]), float(string[3])))
        if string[0] == "f":
            for i in range(1, len(string)):
                trix.append(int(string[i].split("/")[0]))
        if string[0] == "l":
            edges.extend([int(string[1]), int(string[2])])

    file.close()

    return Mesh(verts, trix, edges)


class GameWindow:
    def __init__(self, size: Vector2 = Vector2(800, 600), max_fps: int = 0):
        self.clock = pg.time.Clock()
        self.screen = None
        self.size = size
        self.max_fps = max_fps

    def run(self):
        self.screen = pg.display.set_mode(self.size.get_tuple(), DOUBLEBUF | OPENGL | GL_RGB)
        gluPerspective(90, (self.size.x / self.size.y), 0.01, 1000.0)

        move_speed = 3

        world = from_obj("models/map.obj")
        cube = from_obj("models/edgyasscube.obj")
        monke = from_obj("models/monke.obj")

        time = 0

        while True:
            delta_time = self.clock.get_time() * 1e-3
            time += delta_time

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    quit()

            matrix_data = glGetDoublev(GL_MODELVIEW_MATRIX)
            player_pos = Vector3(-matrix_data[3][0], -matrix_data[3][1], matrix_data[3][2])

            # Простое перемещение для теста
            pressed_keys = pg.key.get_pressed()

            if pressed_keys[pg.K_w]:
                glTranslatef(0, 0, 1 * delta_time * move_speed)
            if pressed_keys[pg.K_s]:
                glTranslatef(0, 0, -1 * delta_time * move_speed)
            if pressed_keys[pg.K_d]:
                glTranslatef(-1 * delta_time * move_speed, 0, 0)
            if pressed_keys[pg.K_a]:
                glTranslatef(1 * delta_time * move_speed, 0, 0)
            if pressed_keys[pg.K_SPACE]:
                glTranslatef(0, -1 * delta_time, 0)
            if pressed_keys[pg.K_c]:
                glTranslatef(0, 1 * delta_time, 0)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # cube.load_to_opengl_wire()
            world.load_to_opengl_faces()
            # monke.load_to_opengl_faces()

            pg.display.set_caption(f"Yandex3D | fps: {int(self.clock.get_fps())}")
            pg.display.flip()
            self.clock.tick(self.max_fps)
