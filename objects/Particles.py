import utilities.utils
import math
import random


class FountainParticles:
    cnt_particle = 0
    particles = None

    def __init__(self, n, interval):
        self.particles = [0] * 4 * n
        time = 0

        for i in range(0, n):
            theta = utilities.utils.mix_floats(0, math.pi / 6.0, random.random())
            phi = utilities.utils.mix_floats(0, 2 * math.pi, random.random())

            velocity = utilities.utils.mix_floats(1.25, 1.5, random.random())

            self.particles[4 * i] = theta
            self.particles[4 * i + 1] = phi
            self.particles[4 * i + 2] = math.sin(theta) * math.sin(phi)
            self.particles[4 * i + 3] = time
            time += interval
