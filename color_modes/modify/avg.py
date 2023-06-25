from color_modes import ColorMode
from models import FloatColor

class AvgColorMode(ColorMode):
    def __init__(self, a:ColorMode, b:ColorMode):
        if (a == None):
            raise ValueError("Color mode A unset")
        if (b == None):
            raise ValueError("Color mode B unset")

        self.colorModeA = a
        self.colorModeB = b

    def getColor(self, x:float, y:float) -> FloatColor:
        colorA = self.colorModeA.getColor(x, y)
        colorB = self.colorModeB.getColor(x, y)

        return (colorA + colorB) * 0.5