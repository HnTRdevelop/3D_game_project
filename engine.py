import pygame as pg
from pygame.locals import *
from mathf import *
from OpenGL.GL import *
from OpenGL.GLU import *


pg.init()


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
        self.screen = pg.display.set_mode(self.size.get_tuple(), DOUBLEBUF | OPENGL)
        gluPerspective(90, (self.size.x / self.size.y), 0.01, 1000.0)
        glTranslatef(0.0, -1.65, 0.0)

        camera_pos = Vector3()
        rotation = 0.0
        rot_speed = 90
        move_speed = 3

        world = from_obj("map.obj")

        time = 0

        while True:
            delta_time = self.clock.get_time() * 1e-3
            time += delta_time

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    quit()

            pressed_keys = pg.key.get_pressed()
            if pressed_keys[pg.K_LEFT]:
                glRotatef(rot_speed * delta_time, 0, -1, 0)
                rotation += rot_speed * delta_time
            elif pressed_keys[pg.K_RIGHT]:
                glRotatef(rot_speed * delta_time, 0, 1, 0)
                rotation -= rot_speed * delta_time

            if pressed_keys[pg.K_w]:
                camera_pos.z -= cos(radians(rotation)) * move_speed * delta_time
                camera_pos.x -= sin(radians(rotation)) * move_speed * delta_time
            elif pressed_keys[pg.K_s]:
                camera_pos.z += cos(radians(rotation)) * move_speed * delta_time
                camera_pos.x += sin(radians(rotation)) * move_speed * delta_time
            if pressed_keys[pg.K_d]:
                camera_pos.z += cos(radians(rotation + 90)) * move_speed * delta_time
                camera_pos.x += sin(radians(rotation + 90)) * move_speed * delta_time
            elif pressed_keys[pg.K_a]:
                camera_pos.z -= cos(radians(rotation + 90)) * move_speed * delta_time
                camera_pos.x -= sin(radians(rotation + 90)) * move_speed * delta_time

            if pressed_keys[pg.K_SPACE]:
                camera_pos.y += move_speed * delta_time
            elif pressed_keys[pg.K_c]:
                camera_pos.y -= move_speed * delta_time

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            world.load_to_opengl_faces(camera_pos)

            pg.display.set_caption(f"Yandex3D | fps: {int(self.clock.get_fps())}")
            pg.display.flip()
            self.clock.tick(self.max_fps)
