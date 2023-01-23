class ShaderProgram:
    def __init__(self, glcontext):
        self.glcontext = glcontext
        self.programs = {"default": self.get_program("default")}

    def get_program(self, shader_name: str):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.glcontext.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def release_data(self):
        for program in self.programs.values():
            program.release()
