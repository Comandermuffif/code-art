from color_modes import ColorMode
from models import FloatColor, Point

class FireColorMode(ColorMode):
    def __init__(self):
        self.center = Point(0.5, 0.5)

    def getColor(self, x:float, y:float) -> FloatColor:
        if (y > 0.8):
            return FloatColor(0, 0, 0) # Back
        if (x * -0.6 + 0.8 < y and x * 0.6 + 0.2 < y):
            return FloatColor(1, 0, 0) # Red
        return FloatColor(1, 1, 1)