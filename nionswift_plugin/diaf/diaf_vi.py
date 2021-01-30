import numpy

from . import Apertures_controller

__author__ = "Yves Auad"

class Diafs(Apertures_controller.Aperture_Controller):

    def __init__(self):
        pass

    def pos_to_bytes(self, pos):
        rem = pos
        val = numpy.zeros(4, dtype=int)
        for j in range(4):  # 4 bytes
            val[j] = rem % 256
            rem = rem - val[j]
            rem = rem / 256
        return val

    def set_val(self, motor, value):
        byt = self.pos_to_bytes(value)
        message = [motor, 20, byt[0], byt[1], byt[2], byt[3]]
        byt_array = bytearray(message)

    def get_val(self, which):
        pass
