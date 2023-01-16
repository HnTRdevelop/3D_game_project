import numpy as np
import glm
import pygame as pg


class Mesh:
    def __init__(self, app):
        self.vertices = []
        self.triangles = []
        self.texture_vertices = []
        self.texture_triangles = []
        self.texture_coord_data = np.array([], dtype=np.float32)
        self.app = app
        self.glcontext = app.glcontext
        self.from_obj("models/maz500.obj")
        self.vbo = self.get_vbo()
        self.model_matrix = self.get_model_matrix()
        self.texture = self.get_texture("textures/blank.png")
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vao()
        self.on_init()

    def on_init(self):
        self.shader_program["u_texture"] = 0
        self.texture.use()

        self.shader_program["projection_matrix"].write(self.app.camera.get_projection_matrix())
        self.shader_program["view_matrix"].write(self.app.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(self.model_matrix)

    def get_texture(self, texture_path: str):
        texture = pg.image.load(texture_path).convert()
        texture = pg.transform.flip(texture, False, True)
        texture = self.glcontext.texture(size=texture.get_size(),
                                         components=3,
                                         data=pg.image.tostring(texture, "RGB"))
        return texture

    def update(self):
        model_matrix = self.model_matrix
        self.shader_program["model_matrix"].write(model_matrix)
        self.shader_program["view_matrix"].write(self.app.camera.get_view_matrix())

    def render(self):
        self.update()
        self.vao.render()

    def release_data(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.glcontext.vertex_array(self.shader_program, [(self.vbo, "2f 3f",
                                                                 "in_texture_coord", "in_position")])
        return vao

    def get_vertex_data(self):
        vertex_data = self.get_data(self.vertices, self.triangles)
        texture_coord_data = self.get_data(self.texture_vertices, self.texture_triangles)
        vertex_data = np.hstack([texture_coord_data, vertex_data])
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.glcontext.buffer(vertex_data)
        return vbo

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        return model_matrix

    def get_shader_program(self, shader_name: str):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.glcontext.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    @staticmethod
    def get_data(vertices, triangles):
        data = [vertices[ind] for triangle in triangles for ind in triangle]
        return np.array(data, dtype=np.float32)

    def from_obj(self, file_path: str):
        file = open(file_path)

        verts = []
        trix = []
        text_verts = []
        text_trix = []
        for string in file.readlines():
            string = string.split()
            if len(string) == 0:
                continue
            if string[0] == "v":
                verts.append((float(string[1]), float(string[2]), float(string[3])))
            if string[0] == "f":
                triangle = []
                texture_triangle = []
                for i in range(1, len(string)):
                    triangle_data = string[i].split("/")
                    triangle.append(int(triangle_data[0]) - 1)
                    texture_triangle.append(int(triangle_data[1]) - 1)
                trix.append(tuple(triangle))
                text_trix.append(tuple(texture_triangle))
            if string[0] == "vt":
                text_verts.append((float(string[1]), float(string[2])))

        file.close()

        self.vertices = verts
        self.triangles = trix
        self.texture_vertices = text_verts
        self.texture_triangles = text_trix
