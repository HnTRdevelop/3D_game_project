from vao import VAOController
from texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao_controller = VAOController(self.app.glcontext)
        self.texture_controller = Texture(self.app.glcontext)

    def set_vao(self, vao_name: str, shader_name: str, vbo_name: str):
        self.vao_controller.set_vao(vao_name, shader_name, vbo_name)

    def set_vbo(self, vbo_name: str, model_path: str):
        self.vao_controller.vbo_controller.set_vbo(vbo_name, model_path)

    def set_3d_model(self, model_name: str, model_path):
        self.vao_controller.vbo_controller.set_vbo(model_name, model_path)
        self.vao_controller.set_vao(model_name, "default", model_name)

    def set_texture(self, texture_name: str, texture_path: str):
        self.texture_controller.set_texture(texture_name, texture_path)

    def release_data(self):
        self.vao_controller.release_data()
        self.texture_controller.release_data()
