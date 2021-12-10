import sys
from OpenGL.GL import *


class Mesh:
    def __init__(self, cnt):
        self._vertex_array_object = glGenVertexArrays(1)
        self._vertex_array_buffer = glGenBuffers(1)
        self._element_buffer_object = None
        self._draw_count = cnt

    def initialise_particles(self, vertices, vbo):
        self._vertex_array_buffer = vbo
        glBindVertexArray(self._vertex_array_buffer)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_array_buffer)
        glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, GL_DYNAMIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(12))
        glBindVertexArray(0)

    def initialise(self, vertices, indices):
        self._element_buffer_object = glGenBuffers(1)

        glBindVertexArray(self._vertex_array_object)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_array_buffer)
        glBufferData(GL_ARRAY_BUFFER, len(vertices)*len(vertices[0])*5*4, vertices, GL_STATIC_DRAW)
        print(len(vertices)*len(vertices[0])*5*4)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer_object)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices)*4, indices, GL_STATIC_DRAW)
        print(len(indices)*4)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        glBindVertexArray(0)

    def clean_up(self):
        glDeleteBuffers(1, self._vertex_array_buffer)
        glDeleteVertexArrays(1, self._vertex_array_object)

    @property
    def vertex_array_object(self):
        return self._vertex_array_object

    def draw_count(self):
        return self._draw_count

