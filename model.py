import glm


class Model:
    def __init__(self, app, vao_name: str, texture_name: str = None,
                 position: glm.vec3 = glm.vec3(0),
                 rotation: glm.vec3 = glm.vec3(0),
                 scale: glm.vec3 = glm.vec3(1)):
        self.texture = None
        self.position = position
        self.rotation = glm.vec3(glm.radians(rotation.x), glm.radians(rotation.y), glm.radians(rotation.z))
        self.scale = scale
        self.app = app
        self.model_matrix = self.get_model_matrix()
        self.texture_name = texture_name
        self.vao = self.app.mesh.vao_controller.vao_array[vao_name]
        self.shader_program = self.vao.program
        self.camera = self.app.camera
        self.on_init()

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, self.position)

        model_matrix = glm.rotate(model_matrix, self.rotation.x, glm.vec3(1, 0, 0))
        model_matrix = glm.rotate(model_matrix, self.rotation.y, glm.vec3(0, 1, 0))
        model_matrix = glm.rotate(model_matrix, self.rotation.z, glm.vec3(0, 0, 1))

        model_matrix = glm.scale(model_matrix, self.scale)

        return model_matrix

    def on_init(self):
        self.texture = self.app.mesh.texture.texture_array[self.texture_name]
        self.shader_program["u_texture"] = 0
        self.texture.use()

        self.shader_program["projection_matrix"].write(self.camera.projection_matrix)
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(self.model_matrix)

    def update(self):
        self.texture.use()
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(self.model_matrix)

    def render(self):
        self.update()
        self.vao.render()

    def change_scale(self, new_size: glm.vec3):
        self.scale = new_size
        self.model_matrix = self.get_model_matrix()

    def change_position(self, new_position: glm.vec3):
        self.position = new_position
        self.model_matrix = self.get_model_matrix()

    def change_rotation(self, new_rotation: glm.vec3):
        self.rotation = new_rotation
        self.model_matrix = self.get_model_matrix()

