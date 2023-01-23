import glm


class BaseModel:
    def __init__(self, app, vao_name, texture_id=None):
        self.texture = None
        self.app = app
        self.model_matrix = self.get_model_matrix()
        self.texture_id = texture_id
        self.vao = self.app.mesh.vao.vao_array[vao_name]
        self.shader_program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        return model_matrix

    def render(self):
        self.update()
        self.vao.render()


class CubeModel(BaseModel):
    def __init__(self, app, vao_name="cube", texture_id=1):
        super().__init__(app, vao_name, texture_id)
        self.on_init()

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.shader_program["u_texture"] = 0
        self.texture.use()

        self.shader_program["projection_matrix"].write(self.camera.get_projection_matrix())
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(self.model_matrix)

    def update(self):
        self.texture.use()
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(self.model_matrix)
