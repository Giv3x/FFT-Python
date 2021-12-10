import numpy
import random

from OpenGL.GL import *
from PIL import Image


class Texture:
    _texture = None

    def __init__(self):
        return

    def init_texture_location(self, location):
        img = Image.open(location)
        image_data = numpy.array(list(img.getdata()), numpy)

        self._texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 512, 512, GL_FALSE, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    def init_texture_array(self, img, width, height):
        self._texture = glGenTextures(1)
        image_data = numpy.array(img, numpy.float32)
        glBindTexture(GL_TEXTURE_2D, self._texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, GL_FALSE, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    def init_texture_empty(self, width, height, unit):
        self._texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA32F, width, height)
        glBindImageTexture(unit, self._texture, 0, GL_FALSE, 0, GL_READ_WRITE, GL_RGBA32F)

    def clean_up(self):
        glDeleteTextures(1, self._texture)

    def bind_texture_2D(self, unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self._texture)

    def unbind_texture_2D(self, unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, 0)

    @property
    def texture_id(self):
        return self._texture
