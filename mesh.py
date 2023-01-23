from vao import VAOController
from texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao_controller = VAOController(self.app.glcontext)
        self.texture = Texture(self.app.glcontext)

    def release_data(self):
        self.vao_controller.release_data()
        self.texture.release_data()
