import math
import random

from color_modes import ColorMode
from models import FloatColor

class NormalColorMode(ColorMode):
    def __init__(self, child:ColorMode, xDivergance:float=0.1, yDivergance:float=0.1):
        if (child == None):
            raise ValueError("Child color mode unset")
        self.child = child
        self.xDivergance = xDivergance
        self.yDivergance = yDivergance

    def getColor(self, x:float, y:float) -> FloatColor:
        return self.child.getColor(
            max(0, min(1, x + random.normalvariate(0, self.xDivergance))),
            max(0, min(1, y + random.normalvariate(0, self.yDivergance)))
        )