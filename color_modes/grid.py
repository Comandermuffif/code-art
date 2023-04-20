import math

from color_modes import ColorMode
from models import FloatColor

class GridColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor]):
        self.colors = colors
        self.side = int(math.sqrt(len(self.colors)))

    def getColor(self, x:float, y:float) -> FloatColor:
        index = math.floor(x * self.side) + math.floor(y * (self.side + 1)) * self.side
        if index >= len(self.colors):
            index = -1
        return self.colors[index]