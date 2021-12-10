import glfw
from OpenGL.GL import *


class Display:
    def __init__(self, width, height, name, fullScreen):
        if not glfw.init():
            return -1  # resource failed to initialise

        self._width = width
        self._height = height
        self._name = name
        self._aspectRatio = width / height
        self._window = glfw.create_window(width, height, name, fullScreen, None)

        if not self._window:
            glfw.terminate()
            self._closed = True
            return -2  # window failed to initialise
        else:
            self._closed = False

        glfw.make_context_current(self._window)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    def is_closed(self):
        if glfw.window_should_close(self._window):
            self._closed = True
            self.clean_up()
        return self._closed

    def update(self):
        glfw.swap_buffers(self._window)

    def clean_up(self):
        glfw.terminate()

    @property
    def closed(self):
        return self._closed

    def width(self):
        return self._width

    def height(self):
        return self._height
