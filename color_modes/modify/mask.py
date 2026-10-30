import math


from color_modes import ColorMode
from models import FloatColor

class MaskColorMode(ColorMode):
    def __init__(self, inner:ColorMode, outer:ColorMode, radious=0.45):
        self.inner = inner
        self.outer = outer
        self.radious = radious

    def getColor(self, x:float, y:float) -> FloatColor:
        dist = math.sqrt(math.pow(x - 0.5, 2) + math.pow(y - 0.5, 2))
        if dist < self.radious:
            return self.inner.getColor(x, y)
        else:
            return self.outer.getColor(x, y)
