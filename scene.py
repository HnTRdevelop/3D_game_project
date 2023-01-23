from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = {"heap": []}
        self.load()

    def add_object(self, obj, name: str = "heap"):
        if name == "heap":
            self.objects["heap"].append(obj)
        else:
            self.objects[name] = obj

    def get_object(self, name: str) -> Model:
        return self.objects[name] if name != "heap" else None

    def load(self):
        app = self.app

        for x in range(-20, 21):
            for z in range(-20, 21):
                self.add_object(Model(app, vao_name="cube", texture_name="grass",
                                      position=glm.vec3(x * 10, 0, z * 10),
                                      scale=glm.vec3(5, 1, 5),
                                      rotation=glm.vec3(0, 0, 0)))

        self.add_object(Model(app, vao_name="cat", texture_name="cat", position=glm.vec3(0, 1, 0)), "cat")
        self.add_object(Model(app, vao_name="rainbow_dash", position=glm.vec3(0, 5.2, -15)), "rainbow")
        self.add_object(Model(app, vao_name="twilight", position=glm.vec3(0, 5.2, 15)), "twilight")

    def update(self, delta_time: float):
        rotation = glm.radians(glm.vec3(0, 15 * delta_time, 0))
        self.get_object("cat").change_rotation(self.get_object("cat").rotation + rotation)
        rotation = glm.radians(glm.vec3(0, 90 * delta_time, 0))
        self.get_object("rainbow").change_rotation(self.get_object("rainbow").rotation + rotation)
        self.get_object("twilight").change_rotation(self.get_object("twilight").rotation + rotation)

    def render(self):
        for object_key in self.objects.keys():
            if object_key == "heap":
                for obj in self.objects[object_key]:
                    obj.render()
            else:
                self.objects[object_key].render()
