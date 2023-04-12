import math
import random

from color_modes import ColorMode
from models import FloatColor

class NormalColorMode(ColorMode):
    @classmethod
    def get_name(self) -> str:
        return "Normal"

    def __init__(self, child:ColorMode, divergance:float=0.1):
        if (child == None):
            raise ValueError("Child color mode unset")
        self.child = child
        self.divergance = divergance

    def get_color(self, x:float, y:float) -> FloatColor:

        return self.child.get_color(x, y)

        # return self.child.get_color(
        #     max(0, min(1, x + random.normalvariate(0, self.divergance))),
        #     max(0, min(1, y + random.normalvariate(0, self.divergance)))
        # )