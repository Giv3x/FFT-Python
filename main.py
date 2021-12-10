import numpy
import pyrr
import sys

from objects.Particles import FountainParticles

from Display import *
from OpenGL.GL import *
from Mesh import Mesh
from Camera import Camera
from ocean.Ocean_Shader import OceanShader
from utilities.utils import Transform
from Texture import Texture
from Shader import Shader


def main():
    display = Display(1600, 900, 'OpenGL', None)
    if display.closed:
        return -1  # the resource failed to initialise

    # vertices = [[0., 0., 0., 0., 0.],
    #             [1., 0., 0., 1, 0.],
    #             [0., 2., 0., 0., 1],
    #             [1., 2., 0., 1., 1.]]
    # indices = [0, 3, 2, 0, 1, 3]

    N = 256
    L = 1000
    X = 0
    Z = 0
    vertices = [[[0, -1, 0, 0, 0] for x in range(0, N)] for z in range(0, N)]
    vertices = numpy.array(vertices, dtype=numpy.float32)
    vertices[0][0][0] = X
    vertices[0][0][2] = Z
    for x in range(1, N):
        vertices[x][0][0] = X
        vertices[x][0][2] = vertices[x-1][0][2] - float(L/float(N-1))
        vertices[x][0][3] = 0
        vertices[x][0][4] = vertices[x-1][0][4] + float(1/float(N-1))

    for z in range(1, N):
            vertices[0][z][0] = vertices[0][z - 1][0] + float(L/float(N-1))
            vertices[0][z][2] = Z
            vertices[0][z][3] = vertices[0][z - 1][3] + float(1/float(N-1))
            vertices[0][z][4] = 0

    for x in range(1, N):
        for z in range(1, N):
            vertices[x][z][0] = vertices[x][z - 1][0] + float(L/float(N-1))
            vertices[x][z][2] = vertices[x-1][z][2] - float(L/float(N-1))
            vertices[x][z][3] = vertices[x][z - 1][3] + float(1/float(N-1))
            vertices[x][z][4] = vertices[x-1][z][4] + float(1/float(N-1))

    indices = [0 for x in range(0, (N-1)*6) for y in range(0, (N-1))]

    x=0
    y=0
    for x in range(0, N-1):
        for y in range(0, N-1):
            indices[x*6*(N-1)+y*6] = x*(N)+y
            indices[x*6*(N-1)+y*6+1] = (x+1)*(N)+y+1
            indices[x*6*(N-1)+y*6+2] = (x+1)*(N)+y
            indices[x*6*(N-1)+y*6+3] = x*(N)+y
            indices[x*6*(N-1)+y*6+4] = x*(N)+y+1
            indices[x*6*(N-1)+y*6+5] = (x+1)*(N)+y+1

    print(indices[0])
    print(vertices[0])

    indices = numpy.array(indices, dtype=numpy.uint32)
    bit_reversed_indices = [0]*N
    i = 2
    while i <= N:
        for j in range(1, int(i/2)+1):
            bit_reversed_indices[int(i/2)-1+j] = bit_reversed_indices[j - 1] + int(N / i)
        i *= 2
    bit_reversed_indices = numpy.array(bit_reversed_indices, dtype=numpy.uint32)

    # Initialise shaders
    ocean = OceanShader(256,bit_reversed_indices)
    ocean.get_uniform_locations()

    # Initialise textures
    mesh = Mesh((N-2)*6*(N-1)+(N-2)*6+5+1)
    mesh.initialise(vertices, indices)
    transform = Transform()
    camera = Camera(pyrr.vector3.create(30, 100, 100), 70, display.width() / display.height(), 0.1, 1000)

    ocean.ocean_shader.bind()
    ocean.bind_ocean_shader_model_uniform(transform.get_model())
    ocean.bind_ocean_shader_perspective_uniform(camera.perspective)
    ocean.ocean_shader.stop()

    ocean.h0k_shader().bind()
    ocean.bind_h0k_shader_textures()
    glDispatchCompute(16, 16, 1)
    glMemoryBarrier(GL_ALL_BARRIER_BITS)
    ocean.unbind_h0k_shader_textures()
    ocean.h0k_shader().stop()

    vbo = glGenBuffers(1)
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, vbo)
    glBufferData(GL_SHADER_STORAGE_BUFFER, sys.getsizeof(bit_reversed_indices), bit_reversed_indices, GL_STATIC_DRAW)

    ocean.twidle_factors().bind()
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, vbo)
    ocean.bind_twidle_factors_shader_textures()
    glDispatchCompute(8, 16, 1)
    glMemoryBarrier(GL_ALL_BARRIER_BITS)
    ocean.unbind_twidle_factors_shader_textures()
    ocean.twidle_factors().stop()


    time = 0

    while not display.is_closed():
        ocean.hkt_shader().bind()
        ocean.bind_hkt_shader_time_uniform(time)
        ocean.bind_hkt_shader_textures()
        glDispatchCompute(16, 16, 1)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)
        ocean.unbind_hkt_shader_textures()
        ocean.hkt_shader().stop()

        ping_pong = 0
        for i in range(0, 8):
            ocean.butterfly().bind()
            ocean.bind_butterfly_shader_textures()
            ping_pong %= 2
            ocean.bind_butterfly_shader_stage_uniform(i)
            ocean.bind_butterfly_shader_pingpong_uniform(ping_pong)
            ocean.bind_butterfly_shader_direction_uniform(0)
            glDispatchCompute(16, 16, 1)
            glMemoryBarrier(GL_ALL_BARRIER_BITS)
            ping_pong += 1
            ocean.butterfly().stop()

        for i in range(0, 8):
            ping_pong %= 2
            ocean.butterfly().bind()
            ocean.bind_butterfly_shader_textures()
            ocean.bind_butterfly_shader_stage_uniform(i)
            ocean.bind_butterfly_shader_pingpong_uniform(ping_pong)
            ocean.bind_butterfly_shader_direction_uniform(1)
            glDispatchCompute(16, 16, 1)
            glMemoryBarrier(GL_ALL_BARRIER_BITS)
            ping_pong += 1
            ocean.butterfly().stop()

        ping_pong %= 2
        ocean.inversion().bind()
        ocean.bind_inversion_shader_textures()
        ocean.bind_inversion_shader_pingpong_uniform(0)
        glDispatchCompute(16, 16, 1)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)
        ocean.unbind_inversion_shader_textures()
        ocean.inversion().stop()

        ocean.ocean_shader.bind()
        glBindVertexArray(mesh.vertex_array_object)
        #camera.move([0.0, 0.0, 1.0], 0.1)

        ocean.bind_ocean_shader_view_uniform(camera.get_view_matrix())
        ocean.bind_ocean_shader_textures()
        glDrawElements(GL_LINES, mesh.draw_count(), GL_UNSIGNED_INT, ctypes.c_void_p(0))
        display.update()
        glClearColor(0.1, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glBindVertexArray(0)
        ocean.unbind_ocean_shader_textures()
        ocean.ocean_shader.stop()
        glfw.poll_events()

        time += 0.01

    display.clean_up()
    # shader.clean_up()
    # mesh.clean_up()


if __name__ == '__main__':
    main()
