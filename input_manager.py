import pygame as pg
from glm import vec2


class Inputs:
    pressed_keys = []
    mouse_move = vec2(0)

    @staticmethod
    def get_inputs():
        Inputs.pressed_keys = pg.key.get_pressed()
        Inputs.mouse_move = vec2(pg.mouse.get_rel())
