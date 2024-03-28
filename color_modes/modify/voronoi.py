from random import random

from color_modes import ColorMode
from models import FloatColor, Point

class VoronoiColorMode(ColorMode):
    def __init__(self, child:ColorMode, count:int=3000):
        self.child = child
        self.points = [
            Point(random(), random())
            for _ in range(count)
        ]

    def getColor(self, x:float, y:float) -> FloatColor:
        p = Point(x, y)

        nearest_point:Point = self.points[0]
        nearest_distance = p.distance(nearest_point)
        for point in self.points:
            distance = p.distance(point)
            if distance < nearest_distance:
                nearest_point = point
                nearest_distance = distance

        return self.child.getColor(*nearest_point.as_tuple())