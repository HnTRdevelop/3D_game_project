import numpy as np


class VBOController:
    def __init__(self, glcontext):
        self.vbo_array = {"cat": CubeVBO(glcontext),
                          "cube": CubeVBO(glcontext)}

    def release_data(self):
        for vbo in self.vbo_array.values():
            vbo.release_data()


class BaseVBO:
    def __init__(self, glcontext):
        self.glcontext = glcontext
        self.vertices = []
        self.triangles = []
        self.texture_vertices = []
        self.texture_triangles = []
        self.vbo = self.get_vbo()
        self.format = "2f 3f"
        self.attributes = ["in_texture_coord", "in_position"]

    def get_vertex_data(self): ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.glcontext.buffer(vertex_data)
        return vbo

    @staticmethod
    def get_data(vertices, triangles):
        data = [vertices[ind] for triangle in triangles for ind in triangle]
        return np.array(data, dtype=np.float32)

    def release_data(self):
        self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self, glcontext):
        super().__init__(glcontext)

    def get_vertex_data(self):
        self.from_obj("models/cube.obj")
        vertex_data = self.get_data(self.vertices, self.triangles)
        texture_coord_data = self.get_data(self.texture_vertices, self.texture_triangles)
        vertex_data = np.hstack([texture_coord_data, vertex_data])
        return vertex_data

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
                    if triangle_data[1] != "":
                        texture_triangle.append(int(triangle_data[1]) - 1)
                    else:
                        texture_triangle.append(0)
                trix.append(tuple(triangle))
                text_trix.append(tuple(texture_triangle))
            if string[0] == "vt":
                text_verts.append((float(string[1]), float(string[2])))

        file.close()

        self.vertices = verts
        self.triangles = trix
        self.texture_vertices = text_verts
        self.texture_triangles = text_trix
