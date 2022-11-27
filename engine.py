import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3
import sys
import math


# @ti.kernel
# def compute_matrix4x4(vec: vec3, matrix: ti.types.ndarray()) -> vec3:
#     new_vec = vec3(0.0, 0.0, 0.0)
    
#     new_vec.x = matrix[0, 0] * vec.x + matrix[1, 0] * vec.y + matrix[2, 0] * vec.z + matrix[3, 0]
#     new_vec.y = matrix[0, 1] * vec.x + matrix[1, 1] * vec.y + matrix[2, 1] * vec.z + matrix[3, 1]
#     new_vec.z = matrix[0, 2] * vec.x + matrix[1, 2] * vec.y + matrix[2, 2] * vec.z + matrix[3, 2]
#     w = matrix[0, 3] * vec.x + matrix[1, 3] * vec.y + matrix[2, 3] * vec.z + matrix[3, 3]
    
#     if w != 0:
#         new_vec = vec3(new_vec.x / w, new_vec.y / w, new_vec.z / w)

#     return new_vec

# @ti.kernel
# def convert_to_screen_space(vec: vec3, screen_size: vec2) -> vec2:
#     return screen_size * 0.5 - vec2(vec.x * screen_size.x * 0.5, vec.y * screen_size.y * 0.5)

# @ti.kernel
# def rotate_x(vec: vec3, angle: ti.float32, matrix: ti.types.ndarray()):
#     angle_rad = angle * (math.pi / 180)

#     for i in range(4):
#         for j in range(4):
#             matrix[i, j] = 0
    
#     matrix[0, 0] = 1
#     matrix[1, 1] = ti.cos(angle_rad)
#     matrix[2, 2] = ti.cos(angle_rad)
#     matrix[2, 1] = -ti.sin(angle_rad)
#     matrix[1, 2] = ti.sin(angle_rad)
    

# @ti.kernel
# def rotate_y(vec: vec3, angle: ti.float32, matrix: ti.types.ndarray()):
#     angle_rad = angle * (math.pi / 180)

#     for i in range(4):
#         for j in range(4):
#             matrix[i, j] = 0
    
#     matrix[1, 1] = 1
#     matrix[0, 0] = ti.cos(angle_rad)
#     matrix[2, 2] = ti.cos(angle_rad)
#     matrix[0, 2] = -ti.sin(angle_rad)
#     matrix[2, 0] = ti.sin(angle_rad)
    
    
# @ti.kernel
# def rotate_z(vec: vec3, angle: ti.float32, matrix: ti.types.ndarray()):
#     angle_rad = angle * (math.pi / 180)

#     for i in range(4):
#         for j in range(4):
#             matrix[i, j] = 0
    
#     matrix[2, 2] = 1
#     matrix[0, 0] = ti.cos(angle_rad)
#     matrix[1, 1] = ti.cos(angle_rad)
#     matrix[1, 0] = -ti.sin(angle_rad)
#     matrix[0, 1] = ti.sin(angle_rad)
PROJECTION_MATRIX = np.ndarray(shape=(4, 4), dtype=np.float32)


def from_obj(file_name: str) -> list:
    array = []
    with open(file_name) as file:
        lines = file.read().split("\n")
        for line in lines:
            if line[0:2] != "v ":
                continue
            line = line.split(" ")
            array.append(vec3(float(line[1]), float(line[2]), float(line[3])))
    return array


@ti.data_oriented
class Shader:
    def __init__(self, window):
        self.window = window
        self.screen_size = window.screen_size
        
        self.srceen_array = np.full((*self.screen_size, 3), [0, 0, 0], np.uint8)

        self.screen_field = ti.Vector.field(3, ti.uint8, self.screen_size)
        self.verticies_buffer = ti.Vector.field(3, ti.float32, 1)

    @ti.kernel
    def render(self, time: ti.float32):
        # Verticies shader
        for vert_id in range(self.verticies_buffer.shape[0]):
            vert = self.verticies_buffer[vert_id]

            new_vert = vec3(0.0, 0.0, 0.0)
    
            new_vert.x = PROJECTION_MATRIX[0, 0] * vert.x + PROJECTION_MATRIX[1, 0] * vert.y + \
                         PROJECTION_MATRIX[2, 0] * vert.z + PROJECTION_MATRIX[3, 0]
            new_vert.y = PROJECTION_MATRIX[0, 1] * vert.x + PROJECTION_MATRIX[1, 1] * vert.y + \
                         PROJECTION_MATRIX[2, 1] * vert.z + PROJECTION_MATRIX[3, 1]
            new_vert.z = PROJECTION_MATRIX[0, 2] * vert.x + PROJECTION_MATRIX[1, 2] * vert.y + \
                         PROJECTION_MATRIX[2, 2] * vert.z + PROJECTION_MATRIX[3, 2]
            w = PROJECTION_MATRIX[0, 3] * vert.x + PROJECTION_MATRIX[1, 3] * vert.y + \
                PROJECTION_MATRIX[2, 3] * vert.z + PROJECTION_MATRIX[3, 3]
            
            if w != 0:
                new_vert = vec3(new_vert.x / w, new_vert.y / w, new_vert.z / w)


        # Fragment shader
        for frag_coord in ti.grouped(self.screen_field):
            uv = frag_coord / self.screen_size

            col = 0.5 + 0.5 * ts.cos(time + vec3(uv.x, uv.y, uv.x) + vec3(0, 2, 4))

            self.screen_field[frag_coord.x, self.screen_size.y - frag_coord.y] = col * 255

    def update(self):
        self.render(pg.time.get_ticks() * 1e-03)
        self.srceen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.window.screen, self.srceen_array)

    def run(self):
        self.update()
        self.draw()

    def set_verticies_buffer(self, verticies):
        self.verticies_buffer = ti.Vector.field(3, ti.float32, len(verticies))
        for id in range(len(verticies)):
            self.verticies_buffer[id] = verticies[id]


class GameWindow:
    def __init__(self, screen_size: tuple[int, int], framerate_limit: int = 0) -> None:
        ti.init(arch=ti.cuda)
        pg.init()
        pg.font.init()

        self.screen_size = vec2(*screen_size)
        self.framerate_limit = framerate_limit
    
    def run(self):
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("3D game")
        
        self.clock = pg.time.Clock()

        znear = 0.01
        zfar = 1000.0
        fov = 90.0
        
        f = 1.0 / math.tan((fov * 0.5) * (math.pi / 180.0))
        a = self.screen_size.y / self.screen_size.x

        PROJECTION_MATRIX[0, 0] = a * f
        PROJECTION_MATRIX[1, 1] = f
        PROJECTION_MATRIX[2, 2] = zfar / (zfar - znear)
        PROJECTION_MATRIX[3, 2] = (-znear * zfar) / (zfar - znear)
        PROJECTION_MATRIX[2, 3] = 1

        mesh = np.array(from_obj("monke.obj"))
        shader = Shader(self)
        shader.set_verticies_buffer(mesh)

        font = pg.font.Font(pg.font.get_default_font(), 32)

        while True:
            delta_time = self.clock.get_time() / 1000.0
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))

            shader.run()

            self.screen.blit(font.render(f"fps: {int(self.clock.get_fps())}", True, (255, 255, 255), (0, 0, 0)), (6, 6))
            pg.display.set_caption(f"3D game | fps: {int(self.clock.get_fps())}")

            self.clock.tick(self.framerate_limit)
            pg.display.flip()
