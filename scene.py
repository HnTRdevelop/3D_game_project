import glm
from components import *
from resources_loader import ResourceLoader
import json


COMPONENTS_BINDINGS = {
    "Model": Model.load_from_json, 
    "Transform": Transform.load_from_json
}


class GameObject:
    unique_id = 0

    def __init__(self, name: str = f"GameObject{unique_id}"):
        self.unique_id = GameObject.unique_id = GameObject.unique_id + 1
        self.components = {}
        self.child_array: list[GameObject] = []
        self.parent: GameObject = None
        self.transform = self.set_component(Transform(self))
        self.name = name
        self.start()

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

    def _update(self, delta_time: float):
        self.update(delta_time)
        self._update_childs(delta_time)

    def _update_childs(self, delta_time: float):
        for child in self.child_array:
            child._update(delta_time)

    def render(self, light_sources_data):
        model_component = self.get_component("Model")
        if model_component is not None:
            model_component.render(light_sources_data)
        self.render_childs(light_sources_data)

    def render_childs(self, light_sources_data):
        for child in self.child_array:
            child.render(light_sources_data)

    def start(self): ...
    def update(self, delta_time: float): ...

    def get_data_json(self) -> dict:
        data = {
            "id": self.unique_id,
            "name": self.name,
            "child_array": [],
            "components": []
        }

        for child in self.child_array:
            data["child_array"].append(child.get_data_json())

        for component in self.components.values():
            data["components"].append(component.get_data_json())

        return data
    
    def load_data_from_json(data: dict):
        i = GameObject.unique_id
        gm = GameObject(data["name"])
        gm.unique_id = data["id"]
        for component_data in data["components"]:
            comp = COMPONENTS_BINDINGS[component_data["type"]](component_data, gm)
            if component_data["type"] == "Transform":
                gm.transform.position = comp.position
                gm.transform.rotation = comp.rotation
                gm.transform.scale = comp.scale
            else:
                gm.set_component(comp)
        
        for child_data in data["child_array"]:
            gm.add_child(GameObject.load_data_from_json(child_data))

        GameObject.unique_id = i
        return gm


class LightSource:
    def __init__(self, position: glm.vec3 = glm.vec3(0), color: glm.vec3 = glm.vec3(1)):
        self.position = position
        self.color = color

    def get_light_data(self) -> tuple[glm.vec3, glm.vec3]:
        return self.position, self.color
    
    def get_data_json(self) -> dict:
        return {
            "position": self.position.to_tuple(),
            "color": self.color.to_tuple()
        }
    
    def load_from_from_json(data: dict):
        return LightSource(glm.vec3(data["position"]), glm.vec3(data["color"]))


class Scene:
    def __init__(self, name: str = "None"):
        self.name = name

        self.app = StaticData.app
        self.game_object_array: list[GameObject] = []
        self.light_source_array: list[LightSource] = []
        self.player = StaticData.player
        self.add_object(self.player)
        self.on_load()

    def add_object(self, obj: GameObject) -> GameObject:
        self.game_object_array.append(obj)
        return obj

    def add_light_source(self, light_source) -> LightSource:
        self.light_source_array.append(light_source)
        return light_source

    def get_light_by_id(self, light_id: int) -> LightSource:
        if 0 <= light_id < len(self.light_source_array):
            return self.light_source_array[light_id]
        return None

    def get_object_by_id(self, obj_id: int) -> GameObject:
        if 0 <= obj_id < len(self.game_object_array):
            return self.game_object_array[obj_id]
        return None

    def get_object_by_name(self, obj_name: str) -> GameObject:
        for obj in self.game_object_array:
            if obj.name == obj_name:
                return obj
        return None

    def on_load(self):
        self.start()

    def _update(self, delta_time: float):
        self.update(delta_time)
        self.player.update(delta_time)
        for game_object in self.game_object_array:
            game_object._update(delta_time)

    def render(self):
        light_sources_data = []
        for light_source in self.light_source_array:
            light_sources_data.append(light_source.get_light_data())
        for obj in self.game_object_array:
            obj.render(light_sources_data)

    def start(self): ...
    def update(self, delta_time: float): ...

    def save_to_file(self, file_name: str = None, path_to_save: str = "./"):
        file_name = self.name if file_name is None else file_name
        data = { 
            "name": self.name,
            "game_objects": [],
            "light_sources": [],
            "player_data": {
                "position": self.player.transform.position.to_tuple(),
                "camera_yaw": self.player.camera.yaw,
                "camera_pitch": self.player.camera.pitch
            }
        }
        for object in self.game_object_array:
            if object.unique_id == 1:
                continue
            data["game_objects"].append(object.get_data_json())

        for light_source in self.light_source_array:
            data["light_sources"].append(light_source.get_data_json())

        with open(path_to_save + file_name + ".json", "w") as file:
            json_data = json.dumps(data)
            file.write(json_data)

    def load_scene_from_file(file_path: str):
        scene = Scene()

        data = None
        try:
            with open(file_path, "r") as file:
                data = json.loads(file.read())
                scene.name = data["name"]
        except FileExistsError:
            print("Failed to open file!")
        except FileNotFoundError:
            print("Failed to open file!")

        scene.name = data["name"]

        scene.player.transform.position = glm.vec3(data["player_data"]["position"])
        scene.player.camera.yaw = data["player_data"]["camera_yaw"]
        scene.player.camera.pitch = data["player_data"]["camera_pitch"]

        for gm in data["game_objects"]:
            scene.add_object(GameObject.load_data_from_json(gm))

        for light in data["light_sources"]:
            scene.add_light_source(LightSource.load_from_from_json(light))
        
        return scene
