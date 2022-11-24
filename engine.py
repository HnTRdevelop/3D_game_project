import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3, vec4
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
            
            col = 0.5 + 0.5 * ti.cos(time + vec3(uv.x, uv.y, uv.x) + vec3(0, 2, 4))
            
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

        self.shader = Shader(self)

        while True:
            delta_time = self.clock.get_time() / 1000
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill((30, 30, 30))
            
            self.shader.run()
            
            pg.display.set_caption(f"3D game | fps: {int(self.clock.get_fps())}")
            self.clock.tick(self.framerate_limit)
            pg.display.flip()
