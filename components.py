import glm
from math import *
import numpy as np
from static_data import StaticData


class BaseComponent:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def get_data_json() -> dict: ...
    def load_from_json(data, owner): ...


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
    
    def rescale(self, new_scale: glm.vec3):
        self.scale = new_scale

    def get_data_json(self) -> dict:
        return {
            "type": "Transform",
            "position": self.position.to_tuple(),
            "rotation": self.rotation.to_tuple(),
            "scale": self.scale.to_tuple()
        }
    
    def load_from_json(data, owner):
        transform = Transform(owner)
        transform.position = glm.vec3(data["position"])
        transform.rotation = glm.vec3(data["rotation"])
        transform.scale = glm.vec3(data["scale"])

        return transform


class Model(BaseComponent):
    def __init__(self, owner, vao_name: str, texture_name: str = "none"):
        super().__init__("Model", owner)
        self.texture = None
        self.app = StaticData.app
        self.texture_name = texture_name
        self.vao_name = vao_name
        self.vao = self.app.mesh.vao_controller.vao_array[self.vao_name]
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

    def update(self, light_sources_data):
        model_matrix = self.get_model_matrix()
        self.texture.use()
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(model_matrix)
        self.shader_program["view_pos"].write(self.camera.position)

        self.shader_program["light_count"] = len(light_sources_data)
        lights = [glm.vec3(0) for _ in range(128)]
        colors = [glm.vec3(0) for _ in range(128)]
        for i in range(len(light_sources_data)):
            lights[i] = light_sources_data[i][0]
            colors[i] = light_sources_data[i][1]
        self.shader_program["light_sources"].write(np.array(lights))
        self.shader_program["light_colors"].write(np.array(colors))

    def render(self, light_sources_data):
        self.update(light_sources_data)
        self.vao.render()

    def get_data_json(self) -> dict:
        return {
            "type": "Model",
            "texture_name": self.texture_name,
            "vao_name": self.vao_name
        }
    
    def load_from_json(data, owner):
        return Model(owner, data["vao_name"], data["texture_name"])

    def update_texture(self, texture_name):
        self.texture_name = texture_name
        self.on_init()
