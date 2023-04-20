import math

from color_modes import ColorMode
from models import FloatColor

class GradientColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor]):
        self.colors = colors

    def getColor(self, x:float, y:float) -> FloatColor:
        buckets = len(self.colors)
        index = math.floor(x * buckets)
        if (index == buckets):
            return self.colors[-1]
        return self.colors[index]