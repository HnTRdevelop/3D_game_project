import numpy as np
import glm


class Mesh:
    def __init__(self, app):
        self.app = app
        self.glcontext = app.glcontext
        self.vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                         (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        self.indices = [(0, 2, 3), (0, 1, 2),
                        (1, 7, 2), (1, 6, 7),
                        (6, 5, 4), (4, 7, 6),
                        (3, 4, 5), (3, 5, 0),
                        (3, 7, 4), (3, 2, 7),
                        (0, 6, 1), (0, 5, 6)]
        self.vbo = self.get_vbo()
        self.model_matrix = self.get_model_matrix()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vao()
        self.on_init()

    def on_init(self):
        self.shader_program["projection_matrix"].write(self.app.camera.projection_matrix)
        self.shader_program["view_matrix"].write(self.app.camera.view_matrix)
        self.shader_program["model_matrix"].write(self.model_matrix)

    def update(self):
        model_matrix = glm.rotate(self.model_matrix, self.app.time, glm.vec3(0, 1, 0))
        model_matrix *= glm.rotate(self.model_matrix, self.app.time * 3, glm.vec3(1, 0, 0))
        model_matrix *= glm.rotate(self.model_matrix, self.app.time, glm.vec3(0, 0, 1))
        self.shader_program["model_matrix"].write(model_matrix)

    def render(self):
        self.update()
        self.vao.render()

    def release_data(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.glcontext.vertex_array(self.shader_program, [(self.vbo, "3f", "in_position")])
        return vao

    def get_vertex_data(self):
        vertex_data = self.get_data(self.vertices, self.indices)
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.glcontext.buffer(vertex_data)
        return vbo

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        return model_matrix

    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.glcontext.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype=np.float32)
