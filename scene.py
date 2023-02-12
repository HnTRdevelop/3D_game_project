import glm
from components import *


class GameObject:
    unique_id = 0

    def __init__(self, name: str = f"GameObject{unique_id}"):
        GameObject.unique_id += 1
        self.components = {}
        self.child_array: list[GameObject] = []
        self.parent: GameObject = None
        self.transform = self.set_component(Transform(self))
        self.name = name

    def get_component(self, component: str):
        if component not in self.components.keys():
            return None
        return self.components[component]

    def set_component(self, component):
        self.components[component.name] = component
        return component

    def add_child(self, child):
        self.child_array.append(child)
        child.parent = self

    def get_child_by_id(self, child_id: int):
        if 0 <= child_id < len(self.child_array):
            return self.child_array[child_id]
        return None

    def get_child_by_name(self, child_name: str):
        for child in self.child_array:
            if child.name == child_name:
                return child
        return None

    def update(self, delta_time: float):
        self.update_childs(delta_time)

    def update_childs(self, delta_time: float):
        for child in self.child_array:
            child.update(delta_time)

    def render(self, light_sources_data):
        model_component = self.get_component("Model")
        if model_component is not None:
            model_component.render(light_sources_data)
        self.render_childs(light_sources_data)

    def render_childs(self, light_sources_data):
        for child in self.child_array:
            child.render(light_sources_data)


class LightSource:
    def __init__(self, position: glm.vec3 = glm.vec3(0), color: glm.vec3 = glm.vec3(1)):
        self.position = position
        self.color = color

    def get_light_data(self):
        return self.position, self.color


class Scene:
    def __init__(self, app, player):
        self.app = app
        self.game_object_array: list[GameObject] = []
        self.light_source_array: list[LightSource] = []
        self.player = player
        self.add_object(self.player)
        self.on_load()

    def add_object(self, obj: GameObject) -> GameObject:
        self.game_object_array.append(obj)
        return obj

    def add_light_source(self, light_source) -> LightSource:
        self.light_source_array.append(light_source)
        return light_source

    def get_light_by_id(self, light_id: int):
        if 0 <= light_id < len(self.light_source_array):
            return self.light_source_array[light_id]
        return None

    def get_object_by_id(self, obj_id: int):
        if 0 <= obj_id < len(self.game_object_array):
            return self.game_object_array[obj_id]
        return None

    def get_object_by_name(self, obj_name: str):
        for obj in self.game_object_array:
            if obj.name == obj_name:
                return obj
        return None

    def on_load(self):
        app = self.app

        self.add_light_source(LightSource(glm.vec3(0, 8, 0), glm.vec3(0, 1, 0)))
        self.add_light_source(LightSource(glm.vec3(0, -12, 0), glm.vec3(1, 0, 0)))

        for x in range(-5, 6):
            for z in range(-5, 6):
                cat = GameObject(f"cat({x}, {z})")
                cat.set_component(Model(app, cat, "cat_model", "cat_texture"))
                cat.transform.position = glm.vec3(x * 10, -2, z * 10)
                cat.transform.scale = glm.vec3(0.5, 0.5, 0.5)
                self.add_object(cat)

    def update(self, delta_time: float):
        self.player.update(delta_time)
        for game_object in self.game_object_array:
            game_object.update(delta_time)

    def render(self):
        light_sources_data = []
        for light_source in self.light_source_array:
            light_sources_data.append(light_source.get_light_data())
        for obj in self.game_object_array:
            obj.render(light_sources_data)
