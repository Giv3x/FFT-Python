import numpy
import pyrr

class Camera:
    _perspective = None
    _position = [float(0.0), float(0.0), float(0.1)]
    _forward = pyrr.vector3.create(60, 30, -50)
    _up = pyrr.vector3.create(0, 1, 0)
    _y_axis = pyrr.vector3.create(0, 1, 0)

    def __init__(self, pos, fov, ratio, z_near, z_far):
        self._perspective = pyrr.matrix44.create_perspective_projection_matrix(fov, ratio, z_near, z_far)
        self._position = numpy.array(pos, dtype=numpy.float64)

    def get_view_matrix(self):
        return pyrr.matrix44.create_look_at(self._position, self._forward, self._up)

    def move(self, dir, amt):
        self._position[0] += dir[0] * amt
        self._position[1] += dir[1] * amt
        self._position[2] += dir[2] * amt

    @property
    def perspective(self):
        return self._perspective
