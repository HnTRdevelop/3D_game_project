import glm


class BaseModel:
    def __init__(self, app, vao_name, texture_id, pos=glm.vec3(0), rot=glm.vec3(0), scale=glm.vec3(1)):
        self.texture = None
        self.pos = pos
        self.rot = glm.vec3(glm.radians(rot.x), glm.radians(rot.y), glm.radians(rot.z))
        self.scale = scale
        self.app = app
        self.model_matrix = self.get_model_matrix()
        self.texture_id = texture_id
        self.vao = self.app.mesh.vao.vao_array[vao_name]
        self.shader_program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, self.pos)

        model_matrix = glm.rotate(model_matrix, self.rot.x, glm.vec3(1, 0, 0))
        model_matrix = glm.rotate(model_matrix, self.rot.y, glm.vec3(0, 1, 0))
        model_matrix = glm.rotate(model_matrix, self.rot.z, glm.vec3(0, 0, 1))

        model_matrix = glm.scale(model_matrix, self.scale)

        return model_matrix

    def render(self):
        self.update()
        self.vao.render()


class CubeModel(BaseModel):
    def __init__(self, app, texture_id=None, pos=glm.vec3(0), rot=glm.vec3(0), scale=glm.vec3(1)):
        super().__init__(app, "cube", texture_id, pos, rot, scale)
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


class CatModel(BaseModel):
    def __init__(self, app, texture_id="cat", pos=glm.vec3(0), rot=glm.vec3(0), scale=glm.vec3(1)):
        super().__init__(app, "cat", texture_id, pos, rot, scale)
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
