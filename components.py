import glm


class BaseComponent:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner


class Transform(BaseComponent):
    def __init__(self, owner):
        super().__init__("Transform", owner)
        self.position = glm.vec3(0)
        self.rotation = glm.vec3(0)
        self.scale = glm.vec3(1)

    def translate(self, translation: glm.vec3):
        self.position += translation

    def rotate(self, rotation: glm.vec3):
        self.rotation += glm.radians(rotation)


class Model(BaseComponent):
    def __init__(self, app, owner, vao_name: str, texture_name: str = None):
        super().__init__("Model", owner)
        self.texture = None
        self.app = app
        self.texture_name = texture_name
        self.vao = self.app.mesh.vao_controller.vao_array[vao_name]
        self.shader_program = self.vao.program
        self.camera = self.app.camera
        self.on_init()

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, self.owner.transform.position)

        model_matrix = glm.rotate(model_matrix, self.owner.transform.rotation.x, glm.vec3(1, 0, 0))
        model_matrix = glm.rotate(model_matrix, self.owner.transform.rotation.y, glm.vec3(0, 1, 0))
        model_matrix = glm.rotate(model_matrix, self.owner.transform.rotation.z, glm.vec3(0, 0, 1))

        model_matrix = glm.scale(model_matrix, self.owner.transform.scale)

        return model_matrix

    def on_init(self):
        self.texture = self.app.mesh.texture_controller.texture_array[self.texture_name]
        self.shader_program["u_texture"] = 0
        self.texture.use()

        self.shader_program["projection_matrix"].write(self.camera.projection_matrix)
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(self.get_model_matrix())

    def update(self):
        model_matrix = self.get_model_matrix()
        self.texture.use()
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(model_matrix)

    def render(self):
        self.update()
        self.vao.render()
