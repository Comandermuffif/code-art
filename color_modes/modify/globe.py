from color_modes import ColorMode
from models import FloatColor, Point

import math

class GlobeColorMode(ColorMode):
    def __init__(self, child:ColorMode, x=0.5, y=0.5, radious=0.4):
        self.child = child
        self.radious = radious
        self.center = Point(x, y)

    def getColor(self, x:float, y:float) -> FloatColor:
        orig = self.child.getColor(x, y)
        dist_center = self.center.distance(Point(x, y))
        if dist_center < self.radious:
            # This makes something cool but not right
            # I don't think this can be done "right" as a grid projected onto a hemisphere
            # looks like a grid in ortholinear space
            scaler = math.sin((dist_center/self.radious) * math.pi / 2)
            return self.child.getColor((x - self.center.x) * scaler + self.center.x, (y - self.center.y) * scaler + self.center.y)
        return orig