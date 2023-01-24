import pygame as pg
import moderngl as gl


class Texture:
    def __init__(self, glcontext):
        self.glcontext = glcontext
        self.texture_array = {None: self.get_texture("textures/placeholder.png")}

    def get_texture(self, texture_path: str):
        texture = pg.image.load(texture_path).convert()
        texture = pg.transform.flip(texture, False, True)
        texture = self.glcontext.texture(size=texture.get_size(),
                                         components=3,
                                         data=pg.image.tostring(texture, "RGB"), )

        texture.filter = (gl.LINEAR_MIPMAP_LINEAR, gl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0

        return texture

    def set_texture(self, texture_name: str, texture_path: str):
        self.texture_array[texture_name] = self.get_texture(texture_path)

    def release_data(self):
        for texture in self.texture_array.values():
            texture.release()
