import pygame as pg
import numpy as np
import taichi as ti
from taichi_glsl import vec2, vec3
import sys
import math


@ti.data_oriented
class Shader:
    def __init__(self, window):
        self.window = window
        self.screen_array = np.full((*self.window.screen_size, 3), [0, 0, 0], np.uint8)

        self.screen_field = ti.Vector.field(3, ti.uint8, self.window.screen_size)

    @ti.kernel
    def render(self, time: ti.float32):
        # Vertex shader
        # idk        
        
        # Fragment shader
        for frag_coord in ti.grouped(self.screen_field):
            uv = frag_coord / self.window.screen_size
            
            col = vec3(0, 1, 0.2)
            
            self.screen_field[frag_coord.x, self.window.screen_size.y - frag_coord.y] = col * 255

    def update(self):
        time = pg.time.get_ticks() * 1e-03
        self.render(time)
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.window.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()


def compute_matrix4x4(vec, matrix):
    new_vec = vec3(0.0, 0.0, 0.0)
    
    new_vec.x = matrix[0, 0] * vec.x + matrix[1, 0] * vec.y + matrix[2, 0] * vec.z + matrix[3, 0]
    new_vec.y = matrix[0, 1] * vec.x + matrix[1, 1] * vec.y + matrix[2, 1] * vec.z + matrix[3, 1]
    new_vec.z = matrix[0, 2] * vec.x + matrix[1, 2] * vec.y + matrix[2, 2] * vec.z + matrix[3, 2]
    w = matrix[0, 3] * vec.x + matrix[1, 3] * vec.y + matrix[2, 3] * vec.z + matrix[3, 3]
    
    if w != 0:
        new_vec = vec3(new_vec.x / w, new_vec.y / w, new_vec.z / w)
        
    return new_vec

def rotate_x(vec, angle):
    angle_rad = angle / 180.0 * math.pi
    
    matrix = np.zeros((4, 4), dtype=np.float32)
    matrix[0, 0] = 1
    matrix[1, 1] = math.cos(angle_rad)
    matrix[2, 2] = math.cos(angle_rad)
    matrix[1, 2] = math.sin(angle_rad)
    matrix[2, 1] = -math.sin(angle_rad)
    
    return compute_matrix4x4(vec, matrix)

def rotate_y(vec, angle):
    angle_rad = angle / 180.0 * math.pi
    
    matrix = np.zeros((4, 4), dtype=np.float32)
    matrix[1, 1] = 1
    matrix[0, 0] = math.cos(angle_rad)
    matrix[2, 0] = math.sin(angle_rad)
    matrix[0, 2] = -math.sin(angle_rad)
    matrix[2, 2] = math.cos(angle_rad)
    
    return compute_matrix4x4(vec, matrix)

def rotate_z(vec, angle):
    angle_rad = angle / 180.0 * math.pi
    
    matrix = np.zeros((4, 4), dtype=np.float32)
    matrix[2, 2] = 1
    matrix[0, 0] = math.cos(angle_rad)
    matrix[1, 1] = math.cos(angle_rad)
    matrix[0, 1] = math.sin(angle_rad)
    matrix[1, 0] = -math.sin(angle_rad)
    
    return compute_matrix4x4(vec, matrix)


class GameWindow:
    def __init__(self, screen_size: tuple[int, int], framerate_limit: int = 0) -> None:
        ti.init(ti.cuda)
        pg.init()
        
        self.screen_size = vec2(*screen_size)
        self.framerate_limit = framerate_limit
    
    def run(self):
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("3D game")
        
        self.clock = pg.time.Clock()

        znear = 0.01
        zfar = 10000.0
        fov = 90.0
        
        f = 1.0 / math.tan((fov / 2.0) / 180.0 * math.pi)
        a = self.screen_size.y / self.screen_size.x

        projection_matrix = np.zeros((4, 4), dtype=np.float32)
        projection_matrix[0, 0] = a * f
        projection_matrix[1, 1] = f
        projection_matrix[2, 2] = zfar / (zfar - znear)
        projection_matrix[3, 2] = (-znear * zfar) / (zfar - znear)
        projection_matrix[2, 3] = 1

        cube = [vec3(-0.5, -0.5, -0.5),
                vec3(-0.5, -0.5, 0.5),
                vec3(-0.5, 0.5, -0.5),
                vec3(-0.5, 0.5, 0.5),
                vec3(0.5, -0.5, -0.5),
                vec3(0.5, -0.5, 0.5),
                vec3(0.5, 0.5, -0.5),
                vec3(0.5, 0.5, 0.5)]

        while True:
            delta_time = self.clock.get_time() / 1000.0
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill((30, 30, 30))
            
            positions = []
            for vert_id in range(len(cube)):
                vert = cube[vert_id]

                projected = compute_matrix4x4(vert + vec3(0, 0, 2), projection_matrix)
                projected = self.screen_size / 2.0 - vec2(projected.x * (self.screen_size.x / 2.0),
                                                          projected.y * (self.screen_size.y / 2.0))
                positions.append(projected)
                
                pg.draw.circle(self.screen, (150, 30, 30), projected, 10)
                
                vert = rotate_x(vert, 90 * delta_time)
                vert = rotate_z(vert, 30 * delta_time)
                vert = rotate_y(vert, 45 * delta_time)
                
                cube[vert_id] = vert
            pg.draw.lines(self.screen, (150, 30, 30), False, positions)
            
            pg.display.set_caption(f"3D game | fps: {int(self.clock.get_fps())}")
            self.clock.tick(self.framerate_limit)
            pg.display.flip()
