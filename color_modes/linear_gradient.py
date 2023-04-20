import colorsys

from color_modes import ColorMode
from models import FloatColor

class LinearGradientColorMode(ColorMode):
    def getColor(self, x:float, y:float) -> FloatColor:
        return FloatColor(*colorsys.hsv_to_rgb((x + y) * 0.5, 1, 1))