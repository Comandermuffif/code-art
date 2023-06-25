import math
from color_modes import ColorMode
from models import FloatColor, Point

class TransformColorMode(ColorMode):
    center = Point(0.5, 0.5)

    def __init__(self, child:ColorMode, xOffset:float=0, yOffset:float=0, xScale:float=1, yScale:float=1, angleDeg:float=0):
        if (child == None):
            raise ValueError("Child color mode unset")
        self.child = child
        self.angleRad = math.radians(angleDeg)

        self.offset = Point(xOffset, yOffset)
        self.scale = Point(xScale, yScale)

    def getColor(self, x:float, y:float) -> FloatColor:
        newPoint = Point(x, y) - self.offset

        delta = newPoint - self.center
        delta = delta / self.scale

        newPoint = self.center + delta
        newPoint = newPoint.rotateAround(self.center, -1 * self.angleRad)

        if newPoint.x < 0 or newPoint.x > 1 or newPoint.y < 0 or newPoint.y > 1:
            return FloatColor(0, 0, 0, 0) # Clear

        return self.child.getColor(newPoint.x, newPoint.y)