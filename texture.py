import pygame as pg
import moderngl as gl


class Texture:
    def __init__(self, glcontext):
        self.glcontext = glcontext
        self.textures = {None: self.get_texture("textures/placeholder.png"),
                         "wooden_box": self.get_texture("textures/box.jpg")}

    def get_texture(self, texture_path):
        texture = pg.image.load(texture_path).convert()
        texture = pg.transform.flip(texture, False, True)
        texture = self.glcontext.texture(size=texture.get_size(),
                                         components=3,
                                         data=pg.image.tostring(texture, "RGB"))
        return texture

    def release_data(self):
        for texture in self.textures.values():
            texture.release()
