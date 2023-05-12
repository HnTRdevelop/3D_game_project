from engine import GameWindow
import pygame as pg
from scene import *


class Program:
    def main():  
        app = GameWindow((1920, 1080), max_fps=0, title="3D engine", show_fps=True)
        player = app.get_player()
        StaticData.player = player

        ResourceLoader.load_model("cube", "models/cube.obj")
        ResourceLoader.load_texture("none", "textures/placeholder.png")

        scene = Scene("Scene")
        cube = scene.add_object(GameObject("cube"))
        cube.set_component(Model(cube, "cube"))
        
        l = scene.add_light_source(LightSource(glm.vec3(3, 3, 3), glm.vec3(0.17, 0.17, 1)))

        app.change_scene(scene)

        app.run()


if __name__ == "__main__":
    Program.main()
