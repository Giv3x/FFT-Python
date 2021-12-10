import random
import numpy

from Shader import Shader
from Texture import Texture
from OpenGL.GL import *


class OceanShader:
    # Shaders
    _ocean_shader = None
    _h0k_shader = None
    _hkt_shader = None
    _twidle_factor_shader = None
    _butterfly_shader = None
    _inversion_shader = None

    # Textures
    _ocean_shader_texture = None
    _h0k_texture = None
    _h0minusk_texture = None
    _hkt_texture = None
    _twidle_factors_texture = None
    _pingpong1_texture = None
    _displacement_texture = None
    _ocean_shader_texture_size = 0

    # Uniforms
    _ocean_shader_uniform_model = None
    _ocean_shader_uniform_view = None
    _ocean_shader_uniform_perspective = None
    _hkt_shader_uniform_time = None
    _h0k_uniform_texture = None
    _h0k_noise_uniform_texture = None
    _h0minusk_uniform_texture = None
    _butterfly_uniform_stage = None
    _butterfly_uniform_pingpong = None
    _butterfly_uniform_direction = None
    _inversion_uniform_pingpong = None

    def __init__(self, size,bit_reversed_indices):
        self._ocean_shader_texture_size = size
        self._ocean_shader = Shader(2)
        self._ocean_shader.initialise_shader_vf("ocean/shaders/ocean", ["position", "texCoords"])
        self._h0k_shader = Shader(1)
        self._h0k_shader.initialise_compute("ocean/shaders/h0k")
        self._hkt_shader = Shader(1)
        self._hkt_shader.initialise_compute("ocean/shaders/hkt")
        self._twidle_factor_shader = Shader(1)
        self._twidle_factor_shader.initialise_compute("ocean/shaders/twidle_factors")
        self._butterfly_shader = Shader(1)
        self._butterfly_shader.initialise_compute("ocean/shaders/butterfly")
        self._inversion_shader = Shader(1)
        self._inversion_shader.initialise_compute("ocean/shaders/inversion")

        self._ocean_shader_texture = Texture()
        self.generate_random_number_texture()
        #self.generate_twidle_texture(bit_reversed_indices)
        self._h0k_texture = Texture()
        self._h0k_texture.init_texture_empty(size, size, 0)
        self._h0minusk_texture = Texture()
        self._h0minusk_texture.init_texture_empty(size, size, 1)
        self._hkt_texture = Texture()
        self._hkt_texture.init_texture_empty(size, size, 2)
        self._twidle_factors_texture = Texture()
        self._twidle_factors_texture.init_texture_empty(8, size, 3)
        self._pingpong1_texture = Texture()
        self._pingpong1_texture.init_texture_empty(size, size, 5)
        self._displacement_texture = Texture()
        self._displacement_texture.init_texture_empty(size, size, 6)

    def get_uniform_locations(self):
        self._ocean_shader_uniform_model = glGetUniformLocation(self._ocean_shader.program, "model")
        self._ocean_shader_uniform_view = glGetUniformLocation(self._ocean_shader.program, "view")
        self._ocean_shader_uniform_perspective = glGetUniformLocation(self._ocean_shader.program, "perspective")
        self._h0k_noise_uniform_texture = glGetUniformLocation(self._h0k_shader.program, "noise")
        self._h0k_uniform_texture = glGetUniformLocation(self._h0k_shader.program, "tilde_h0k")
        self._h0minusk_uniform_texture = glGetUniformLocation(self._h0k_shader.program, "tilde_h0minusk")
        self._hkt_shader_uniform_time = glGetUniformLocation(self._hkt_shader.program, "t")
        self._butterfly_uniform_stage = glGetUniformLocation(self._butterfly_shader.program, "stage")
        self._butterfly_uniform_pingpong = glGetUniformLocation(self._butterfly_shader.program, "pingpong")
        self._butterfly_uniform_direction = glGetUniformLocation(self._butterfly_shader.program, "direction")
        self._inversion_uniform_pingpong = glGetUniformLocation(self._inversion_shader.program, "pingpong")

    def bind_ocean_shader_model_uniform(self, model):
        glUniformMatrix4fv(self._ocean_shader_uniform_model, 1, GL_FALSE, model)

    def bind_ocean_shader_view_uniform(self, view):
        glUniformMatrix4fv(self._ocean_shader_uniform_view, 1, GL_FALSE, view)

    def bind_ocean_shader_perspective_uniform(self, perspective):
        glUniformMatrix4fv(self._ocean_shader_uniform_perspective, 1, GL_FALSE, perspective)

    def bind_hkt_shader_time_uniform(self, time):
        glUniform1f(self._hkt_shader_uniform_time, time)

    def bind_butterfly_shader_stage_uniform(self, stage):
        glUniform1i(self._butterfly_uniform_stage, stage)

    def bind_butterfly_shader_pingpong_uniform(self, pingpong):
        glUniform1i(self._butterfly_uniform_pingpong, pingpong)

    def bind_butterfly_shader_direction_uniform(self, direction):
        glUniform1i(self._butterfly_uniform_direction, direction)

    def bind_inversion_shader_pingpong_uniform(self, pingpong):
        glUniform1i(self._inversion_uniform_pingpong, pingpong)

    def bind_ocean_shader_textures(self):
        self._displacement_texture.bind_texture_2D(0)

    def unbind_ocean_shader_textures(self):
        self._displacement_texture.unbind_texture_2D(0)

    def bind_h0k_shader_textures(self):
        self._h0k_texture.bind_texture_2D(0)
        self._h0minusk_texture.bind_texture_2D(1)
        self._ocean_shader_texture.bind_texture_2D(7)
        glUniform1i(self._h0k_noise_uniform_texture, 7)

    def unbind_h0k_shader_textures(self):
        self._h0k_texture.unbind_texture_2D(0)
        self._h0minusk_texture.unbind_texture_2D(1)
        self._ocean_shader_texture.unbind_texture_2D(7)

    def bind_twidle_factors_shader_textures(self):
        self._twidle_factors_texture.bind_texture_2D(3)

    def unbind_twidle_factors_shader_textures(self):
        self._twidle_factors_texture.unbind_texture_2D(3)

    def bind_hkt_shader_textures(self):
        self._h0k_texture.bind_texture_2D(0)
        self._h0minusk_texture.bind_texture_2D(1)
        self._hkt_texture.bind_texture_2D(2)

    def unbind_hkt_shader_textures(self):
        self._h0k_texture.unbind_texture_2D(0)
        self._h0minusk_texture.unbind_texture_2D(1)
        self._hkt_texture.unbind_texture_2D(2)

    def bind_butterfly_shader_textures(self):
        self._twidle_factors_texture.bind_texture_2D(3)
        self._pingpong1_texture.bind_texture_2D(5)
        self._hkt_texture.bind_texture_2D(2)

    def unbind_butterfly_shader_textures(self):
        self._twidle_factors_texture.unbind_texture_2D(3)
        self._pingpong1_texture.unbind_texture_2D(5)
        self._hkt_texture.unbind_texture_2D(2)

    def bind_inversion_shader_textures(self):
        self._displacement_texture.bind_texture_2D(6)
        self._pingpong1_texture.bind_texture_2D(5)
        self._hkt_texture.bind_texture_2D(2)

    def unbind_inversion_shader_textures(self):
        self._displacement_texture.unbind_texture_2D(6)
        self._pingpong1_texture.unbind_texture_2D(5)
        self._hkt_texture.unbind_texture_2D(2)

    def generate_random_number_texture(self):
        M_PI = 3.1415926535897932384626433832795
        image = [[random.randint(0, 256) for x in range(4 * 256)] for y in range(256)]
        # for i in range(0, len(image)):
        #     for j in range(0, 256):
        #         noise00 = max(min(1.0, image[i][j*4]), 0.0001)
        #         noise01 = max(min(1.0, image[i][j*4+1]), 0.0001)
        #         noise02 = max(min(1.0, image[i][j*4+2]), 0.0001)
        #         noise03 = max(min(1.0, image[i][j*4+3]), 0.0001)
        #         u0 = 8.0 * M_PI * noise00
        #         v0 = 4 * numpy.sqrt(-2.0 * numpy.log(noise01))
        #         u1 = 8.0 * M_PI * noise02
        #         v1 = 4 * numpy.sqrt(-2.0 * numpy.log(noise03))
        #         image[i][j*4] = v0 * numpy.cos(u0)
        #         image[i][j*4+1] = v0 * numpy.sin(u0)
        #         image[i][j*4+2] = v1 * numpy.cos(u1)
        #         image[i][j*4+3] = v1 * numpy.sin(u1)

        self._ocean_shader_texture.init_texture_array(image, self._ocean_shader_texture_size, self._ocean_shader_texture_size)


    def generate_twidle_texture(self, indices):
        M_PI = 3.1415926535897932384626433832795
        width = 8
        N = 256
        image = [[0 for x in range(4 * width)] for y in range(N)]

        for x in range(0, width):
            for y in range(0, N):
                k = numpy.mod(y * (float(N) / pow(2, x + 1)), N)
                real = numpy.cos(2.0*M_PI*k/float(N))
                im = numpy.sin(2.0*M_PI*k/float(N))

                butterflyspan = int(pow(2, x))
                butterflywing = 0
                if numpy.mod(y, pow(2, x + 1)) < pow(2, x):
                    butterflywing = 1

                if x == 0:
                    if(butterflywing):
                        image[y][x * 4] = real
                        image[y][x * 4 + 1] = im
                        image[y][x * 4 + 2] = indices[y]
                        image[y][x * 4 + 3] = indices[y+1]
                    else:
                        image[y][x * 4] = real
                        image[y][x * 4 + 1] = im
                        image[y][x * 4 + 2] = indices[y-1]
                        image[y][x * 4 + 3] = indices[y]
                else:
                    if(butterflywing):
                        image[y][x * 4] = real
                        image[y][x * 4 + 1] = im
                        image[y][x * 4 + 2] = y
                        image[y][x * 4 + 3] = y + butterflyspan
                    else:
                        image[y][x * 4] = real
                        image[y][x * 4 + 1] = im
                        image[y][x * 4 + 2] = y - butterflyspan
                        image[y][x * 4 + 3] = y
        for y in range(0, N):
            print(image[y])

        self._ocean_shader_texture.init_texture_array(image, width, N)

    @property
    def ocean_shader(self):
        return self._ocean_shader

    def h0k_shader(self):
        return self._h0k_shader

    def hkt_shader(self):
        return self._hkt_shader

    def twidle_factors(self):
        return self._twidle_factor_shader

    def butterfly(self):
        return self._butterfly_shader

    def inversion(self):
        return self._inversion_shader

    def ocean_shader_texture(self):
        return self._ocean_shader_texture
