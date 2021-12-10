from enum import Enum

import pyrr
from pyrr import *


class ShaderTypes(Enum):
    VERTEX_SHADER = ".vs"
    FRAGMENT_SHADER = ".fs"


class Transform:
    def __init__(self, pos=[0]*3, rot=[0]*3, scale=[1, 1, 1]):
        self.position = pos
        self.rotation = rot
        self.scale = scale

    def get_model(self):
        transform = pyrr.matrix44.create_from_translation(self.position)

        rot_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        rot_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        rot_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])
        rotate = rot_z * rot_y * rot_x

        scale = pyrr.matrix44.create_from_scale(self.scale)

        return transform * rotate * scale


def mix_floats(x, y, a):
    return x*(1-a) + y*a

