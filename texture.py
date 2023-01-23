import pygame as pg
import moderngl as gl


class Texture:
    def __init__(self, glcontext):
        self.glcontext = glcontext
        self.texture_array = {None: self.get_texture("textures/placeholder.png"),
                              "wooden_box": self.get_texture("textures/box.jpg"),
                              "cat": self.get_texture("textures/cat.jpg"),
                              "grass": self.get_texture("textures/grass.jpg")}

    def get_texture(self, texture_path: str):
        texture = pg.image.load(texture_path).convert()
        texture = pg.transform.flip(texture, False, True)
        texture = self.glcontext.texture(size=texture.get_size(),
                                         components=3,
                                         data=pg.image.tostring(texture, "RGB"),)

        texture.filter = (gl.LINEAR_MIPMAP_LINEAR, gl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0

        return texture

    def release_data(self):
        for texture in self.texture_array.values():
            texture.release()
