from color_modes import ColorMode
from models import FloatColor

class AvgColorMode(ColorMode):
    @classmethod
    def get_name(self) -> str:
        return "Avg"

    def __init__(self, a:ColorMode, b:ColorMode):
        if (a == None):
            raise ValueError("Color mode A unset")
        if (b == None):
            raise ValueError("Color mode B unset")

        self.colorModeA = a
        self.colorModeB = b

    def get_color(self, x:float, y:float) -> FloatColor:
        colorA = self.colorModeA.get_color(x, y)
        colorB = self.colorModeB.get_color(x, y)

        return (colorA + colorB) * 0.5