from OpenGL.GL import * 
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pygame as pg
import sys


# Shaders
vertex_src = """
#version 440

layout(location=0) in vec3 vertPos;
layout(location=1) in vec3 inCol;
out vec3 outCol;

void main()
{
	 gl_Position = vec4(vertPos, 1);

	 outCol = inCol;
}
"""

fragment_src = """
#version 440

in vec3 outCol;
out vec4 fragCol;

void main()
{
	fragCol = vec4(outCol, 1);
}
"""


class GameWindow:
    def __init__(self, screen_size: tuple[int, int], framerate_limit: int = 0) -> None:
        self.screen_size = screen_size
        print(screen_size)
        self.framerate_limit = framerate_limit
    
    def run(self):
        # Инициализируем библиотеки
        pg.init()
        pg.font.init()

        # Создаём окно
        self.screen = pg.display.set_mode(self.screen_size, pg.DOUBLEBUF | pg.OPENGL)
        pg.display.set_caption("3D game")
        glClearColor(60/255, 60/255, 60/255, 1)

        # Создаём Clock
        self.clock = pg.time.Clock()

        triangle = [
             0,  0.5,  0,  255/255, 0/255, 0/255,
            -0.5, -0.5,  0,  0/255, 255/255, 0/255,
             0.5, -0.5,  0,  0/255, 0/255, 255/255]                                                                            

        triangle = np.array(triangle, dtype=np.float32)

        triangle_buffer = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, triangle_buffer)

        glBufferData(GL_ARRAY_BUFFER, triangle.nbytes, triangle, GL_STATIC_DRAW)

        buffer_data = glGetBufferSubData(GL_ARRAY_BUFFER, 0, triangle.nbytes)
        print(buffer_data.view(dtype=np.float32))

        vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)
        shader_program = compileProgram(vertex_shader, fragment_shader)

        glUseProgram(shader_program)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, triangle.itemsize*6, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, triangle.itemsize*6, ctypes.c_void_p(triangle.itemsize*3))

        # Игровой цикл
        while True:
            # Читаем события окна
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # Очищаем экран
            glClear(GL_COLOR_BUFFER_BIT)

            glDrawArrays(GL_TRIANGLES, 0, 3)

            # Обновляем окно
            self.clock.tick(self.framerate_limit)
            pg.display.flip()

