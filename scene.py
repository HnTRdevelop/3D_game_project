from model import *


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
                self.add_object(CubeModel(app, texture_id="wooden_box", pos=glm.vec3(x * 2, 0, z * 2)))

        self.add_object(CatModel(app, texture_id="cat", pos=glm.vec3(0, 1, 0)))

    def render(self):
        for obj in self.objects:
            obj.render()
