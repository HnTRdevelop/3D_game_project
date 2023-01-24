import glm
from components import *


class GameObject:
    unique_id = 0

    def __init__(self, name: str = f"GameObject{unique_id}"):
        GameObject.unique_id += 1
        self.components = {}
        self.transform = self.add_component(Transform(self))
        self.name = name

    def get_component(self, component: str):
        if component not in self.components.keys():
            return None
        return self.components[component]

    def add_component(self, component):
        self.components[component.name] = component
        return component


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects: list[GameObject] = []
        self.load()

    def add_object(self, obj: GameObject) -> GameObject:
        self.objects.append(obj)
        return obj

    def get_object_by_id(self, obj_id: int):
        if 0 <= obj_id < len(self.objects):
            return self.objects[obj_id]
        return None

    def get_object_by_name(self, obj_name: str):
        for obj in self.objects:
            if obj.name == obj_name:
                return obj
        return None

    def load(self):
        app = self.app

        cat = self.add_object(GameObject("Cat"))
        cat.add_component(Model(app, cat, vao_name="cat", texture_name="cat"))

        for x in range(-10, 11):
            for z in range(-10, 11):
                if x == 0 and z == 0:
                    continue
                floor_chunk = self.add_object(GameObject(f"Floor ({x}, {z})"))
                floor_chunk.transform.scale = glm.vec3(10, 1, 10)
                floor_chunk.transform.position = glm.vec3(x * 20, 0, z * 20)
                floor_chunk.add_component(Model(app, floor_chunk, vao_name="cube", texture_name="wooden_box"))

    def update(self, delta_time: float):
        self.get_object_by_id(0).transform.rotate(glm.vec3(0, 90 * delta_time, 0))

    def render(self):
        for obj in self.objects:
            model_component = obj.get_component("Model")
            if model_component is not None:
                model_component.render()
