import random

from color_modes import ColorMode
from models import FloatColor

class RandomColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor]):
        self.colors = colors

    def getColor(self, x:float, y:float) -> FloatColor:
        return random.choice(self.colors)