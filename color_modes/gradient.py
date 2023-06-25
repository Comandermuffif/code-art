import math
import itertools

from color_modes import ColorMode
from models import FloatColor

class GradientColorMode(ColorMode):
    orientations = [
        (1, 1),
        (1, 0),
        (0, 1),
    ]
    scales = [2, 1, 1]

    def __init__(self, colors:list[FloatColor], orientation:int=0):
        self.colors = colors
        self.weights = self.orientations[orientation]
        self.scale = self.scales[orientation]

    def getColor(self, x:float, y:float) -> FloatColor:
        buckets = len(self.colors)
        index = math.floor((x * buckets * self.weights[0] + y * buckets * self.weights[1]) / self.scale)
        if (index == buckets):
            return self.colors[-1]
        return self.colors[index]