from color_modes import ColorMode
from models import FloatColor

class ClampColorMode(ColorMode):
    def __init__(self, child:ColorMode, threshold:float=0.5):
        self.child = child
        self.theshold = threshold

    def getColor(self, x:float, y:float) -> FloatColor:
        orig = self.child.getColor(x, y)
        orig.a = 1 if orig.a >= self.theshold else 0
        return orig