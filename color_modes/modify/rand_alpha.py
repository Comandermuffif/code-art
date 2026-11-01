from random import random

from color_modes import ColorMode
from models import FloatColor

class RandAlphaColorMode(ColorMode):
    def __init__(self, child:ColorMode):
        self.child = child

    def getColor(self, x:float, y:float) -> FloatColor:
        orig = self.child.getColor(x, y)
        if orig.a == 1:
            orig.a = random()
        return orig
