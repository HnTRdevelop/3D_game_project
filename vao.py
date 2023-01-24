from vbo import VBOController
from shader_program import ShaderProgram


class VAOController:
    def __init__(self, glcontext):
        self.glcontext = glcontext
        self.vbo_controller = VBOController(self.glcontext)
        self.shader_program = ShaderProgram(self.glcontext)
        self.vao_array = {}

    def get_vao(self, shader_program, vbo):
        vao = self.glcontext.vertex_array(shader_program, [(vbo.vbo, vbo.format, *vbo.attributes)])
        return vao

    def set_vao(self, vao_name: str, shader_name: str, vbo_name: str):
        self.vao_array[vao_name] = self.get_vao(self.shader_program.programs[shader_name],
                                                self.vbo_controller.vbo_array[vbo_name])

    def release_data(self):
        self.vbo_controller.release_data()
        self.shader_program.release_data()

