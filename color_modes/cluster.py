from math import pow, sqrt
from random import choice, random

from color_modes import ColorMode
from models import FloatColor

class ClusterColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor], count:int=10):
        self.color_points = [
            (random(), random(), choice(colors))
            for _ in range(count)
        ]

    @classmethod
    def _get_distance(cls, point_a:tuple[float, float], point_b:tuple[float, float]) -> float:
        return sqrt(pow(point_a[0] - point_b[0], 2) + pow(point_a[1] - point_b[1], 2))

    def getColor(self, x:float, y:float) -> FloatColor:
        current_point = (x, y)

        distances = [
            (self._get_distance(current_point, color_point[:2]), color_point[2])
            for color_point in self.color_points
        ]

        sorted_distances = sorted(distances, key=lambda a : a[0])
        return sorted_distances[0][1]