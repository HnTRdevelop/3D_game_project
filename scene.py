from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app

        for x in range(-20, 21):
            for z in range(-20, 21):
                self.add_object(Model(app, vao_name="cube", texture_name="grass",
                                          position=glm.vec3(x * 10, 0, z * 10),
                                          scale=glm.vec3(5, 1, 5),
                                          rotation=glm.vec3(0, 90 * x * z, 0)))

        self.cat = Model(app, vao_name="cat", texture_name="cat", position=glm.vec3(0, 3.3, 0))
        self.add_object(self.cat)
        self.cat.change_position(glm.vec3(0, 1, 0))

        self.rainbow = Model(app, vao_name="rainbow_dash", position=glm.vec3(0, 5.2, -15))
        self.add_object(self.rainbow)
        self.twilight = Model(app, vao_name="twilight", position=glm.vec3(0, 5.2, 15))
        self.add_object(self.twilight)

    def update(self, delta_time: float):
        rotation = glm.radians(glm.vec3(0, 15 * delta_time, 0))
        self.cat.change_rotation(self.cat.rotation + rotation)
        rotation = glm.radians(glm.vec3(0, 90 * delta_time, 0))
        self.rainbow.change_rotation(self.rainbow.rotation + rotation)
        self.twilight.change_rotation(self.twilight.rotation - rotation)

    def render(self):
        for obj in self.objects:
            obj.render()
