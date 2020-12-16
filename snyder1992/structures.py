from collections import namedtuple
from math import radians


class Angle(float):

    @property
    def radians(self):
        return radians(self.__float__())

    @property
    def degrees(self):
        return self.__float__()


PolyhedronFace = namedtuple('PolyhedronFace', 'number center_lat center_long center_x center_y polygon')
