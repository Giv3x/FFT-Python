from OpenGL.GL import *
import OpenGL.GL.shaders
from utilities.utils import *


def check_shader_error(program, flag, is_program, error_msg):
    success = 0
    if is_program:
        success = glGetProgramiv(program, flag)
    else:
        success = glGetShaderiv(program, flag)

    if success > 1:
        if is_program:
            print(error_msg + ":" + glGetProgramInfoLog(program, success, None))
        else:
            print(error_msg + ":" + glGetShaderInfoLog(program, success, None))


def create_shader(shader_text, shader_type):
    shader = glCreateShader(shader_type)

    if shader == 0:
        print("Error creating shader type: " + shader_type)
        return 0

    p = [''] * 1
    p[0] = shader_text
    lengths = [0] * 1
    lengths[0] = len(shader_text)

    glShaderSource(shader, p)
    glCompileShader(shader)
    check_shader_error(shader, GL_COMPILE_STATUS, False, "Shader Compilation failed")
    return shader


class Shader:
    _program = 0
    shaders = []

    def __init__(self, size):
        self._program = glCreateProgram()
        self.shaders = [0] * size

    def initialise_shader_vf(self, location, attributes):
        file = open(location + '.vs', "r")
        self.shaders[0] = create_shader(file.read(), GL_VERTEX_SHADER)
        file.close()

        file = open(location + '.fs', "r")
        self.shaders[1] = create_shader(file.read(), GL_FRAGMENT_SHADER)
        file.close()

        for s in self.shaders:
            glAttachShader(self._program, s)

        for i in range(0, len(attributes)):
            glBindAttribLocation(self._program, i, attributes[i])

        glLinkProgram(self._program)
        check_shader_error(self._program, GL_LINK_STATUS, True, "Program linking has failed")

        glValidateProgram(self._program)
        check_shader_error(self._program, GL_VALIDATE_STATUS, True, "Invalid Shader Program")

    def initialise_compute(self, location):
        file = open(location + '.cp', "r")
        self.shaders[0] = create_shader(file.read(), GL_COMPUTE_SHADER)
        file.close()

        for s in self.shaders:
            glAttachShader(self._program, s)

        glLinkProgram(self._program)
        check_shader_error(self._program, GL_LINK_STATUS, True, "Program linking has failed")

        glValidateProgram(self._program)
        check_shader_error(self._program, GL_VALIDATE_STATUS, True, "Invalid Shader Program")

    def clean_up(self):
        for s in self.shaders:
            OpenGL.GL.glDetachShader(self._program, s)
            glDeleteShader(s)

        glDeleteProgram(self._program)

    def bind(self):
        glUseProgram(self._program)

    def stop(self):
        glUseProgram(0)

    @property
    def program(self):
        return self._program

