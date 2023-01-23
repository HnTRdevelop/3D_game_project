from vao import VAO
from texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(self.app.glcontext)
        self.texture = Texture(self.app.glcontext)

    def release_data(self):
        self.vao.release_data()
        self.texture.release_data()
