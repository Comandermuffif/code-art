from color_modes import ColorMode
from models import FloatColor

class ClampColorMode(ColorMode):
    def __init__(self, child:ColorMode):
        self.child = child

    def getColor(self, x:float, y:float) -> FloatColor:
        orig = self.child.getColor(x, y)
        orig.a = 1 if orig.a > 0.5 else 0
        return orig