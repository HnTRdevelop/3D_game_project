from engine import GameWindow
import pygame as pg
from scene import *


class Cube(GameObject):
    def start(self):
        ResourceLoader.load_model("cube", "models/cube.obj")
        self.set_component(Model(self, "cube"))


class RotatinCube(Cube):
    def update(self, delta_time: float):
        direction = glm.vec3(30 * delta_time, 0, 15 * delta_time)
        self.get_component("Transform").rotate(direction)


class Cat(GameObject):
    def start(self):
        ResourceLoader.load_model("cat", "models/cat.obj")
        ResourceLoader.load_texture("cat", "textures/cat.jpg")
        self.set_component(Model(self, "cat", "cat"))


class Program:
    def main():  
        app = GameWindow((1600, 900), max_fps=0, title="3D engine", show_fps=True)
        player = app.get_player()
        StaticData.player = player

        ResourceLoader.load_texture("grass", "textures/grass1.jpg")
        ResourceLoader.load_texture("wood", "textures/wooden_box0.jpg")

        scene = Scene("Scene")
        scene.add_object(RotatinCube("cube")).transform.position = glm.vec3(0, 17, 0)

        obj = scene.add_object(Cube("cube2"))
        obj.get_component("Model").update_texture("grass")
        obj.transform.rescale(glm.vec3(10, 0.5, 10))
        obj.transform.translate(glm.vec3(0, -0.5, 0))
        
        scene.add_object(Cat("cat"))
        
        scene.add_light_source(LightSource(glm.vec3(100, 0, 0), glm.vec3(1, 0, 0)))
        scene.add_light_source(LightSource(glm.vec3(0, 100, 0), glm.vec3(0, 1, 0)))
        scene.add_light_source(LightSource(glm.vec3(0, 0, 100), glm.vec3(0, 0, 1)))

        app.change_scene(scene)

        app.run()


if __name__ == "__main__":
    Program.main()
