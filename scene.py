import glm
from components import *
# from player import Player


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

    def render(self):
        model_component = self.get_component("Model")
        if model_component is not None:
            model_component.render()
        self.render_childs()

    def render_childs(self):
        for child in self.child_array:
            child.render()


class Scene:
    def __init__(self, app, player):
        self.app = app
        self.game_object_array: list[GameObject] = []
        self.player = player
        self.add_object(self.player)
        self.on_load()

    def add_object(self, obj: GameObject) -> GameObject:
        self.game_object_array.append(obj)
        return obj

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
        cat = GameObject("cat")
        cat.set_component(Model(self.app, cat, "cat", "cat"))
        self.add_object(cat)

        cat_child = GameObject("cat_child")
        cat_child.set_component(Model(self.app, cat_child, "cat", "cat"))
        cat_child.transform.scale = glm.vec3(.5, .5, .5)
        cat_child.transform.position = glm.vec3(0, 0, 8)
        cat.add_child(cat_child)

    def update(self, delta_time: float):
        self.player.update(delta_time)
        for game_object in self.game_object_array:
            game_object.update(delta_time)

    def render(self):
        for obj in self.game_object_array:
            obj.render()
