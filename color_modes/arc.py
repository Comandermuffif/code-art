import math

from color_modes import ColorMode
from models import FloatColor, Point

class ArcColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor]):
        self.center = Point(0.5, 0.5)
        self.colors = list(colors)
        colors.reverse()
        self.colors.extend(colors)

    def getColor(self, x:float, y:float) -> FloatColor:
        angle = math.degrees(math.atan2(y - self.center.y, x - self.center.x))
        return self.colors[math.floor(len(self.colors) * angle / 360)]