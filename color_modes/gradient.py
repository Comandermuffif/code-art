import math

from color_modes import ColorMode
from models import FloatColor

class GradientColorMode(ColorMode):
    @classmethod
    def get_name(self) -> str:
        return "Gradient"

    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        self.colors = colors

    def get_color(self, x:float, y:float) -> FloatColor:
        buckets = len(self.colors)
        index = math.floor(x * buckets)
        if (index == buckets):
            return self.colors[-1]
        return self.colors[index]