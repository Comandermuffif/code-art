from color_modes import ColorMode
from models import FloatColor

import math

class AvgColorMode(ColorMode):
    def __init__(self, *colorModes:ColorMode):

        for colorMode in colorModes:
            if (colorMode == None):
                raise ValueError("Color mode unset")

        self.colorModes = colorModes

    def getColor(self, x:float, y:float) -> FloatColor:
        return sum([
            colorMode.getColor(x, y)
            for colorMode in self.colorModes
        ], FloatColor(0, 0, 0)) * (1 / len(self.colorModes))