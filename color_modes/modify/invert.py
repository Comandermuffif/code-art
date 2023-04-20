from color_modes import ColorMode
from models import FloatColor

class InvertColorMode(ColorMode):
    def __init__(self, child:ColorMode):
        self.child = child

    def getColor(self, x:float, y:float) -> FloatColor:
        orig = self.child.getColor(x, y)
        return FloatColor(1 - orig.r, 1 - orig.g, 1 - orig.b)