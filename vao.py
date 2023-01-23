from vbo import VBOController
from shader_program import ShaderProgram


class VAO:
    def __init__(self, glcontext):
        self.glcontext = glcontext
        self.vbo_controller = VBOController(self.glcontext)
        self.shader_program = ShaderProgram(self.glcontext)
        self.vao_array = {
            "cube": self.get_vao(
                self.shader_program.programs["default"],
                self.vbo_controller.vbo_array["cube"]
            )}

    def get_vao(self, shader_program, vbo):
        vao = self.glcontext.vertex_array(shader_program, [(vbo.vbo, vbo.format, *vbo.attributes)])
        return vao

    def release_data(self):
        self.vbo_controller.release_data()
        self.shader_program.release_data()

