import math
from color_modes import ColorMode
from models import FloatColor, Point

class RotateColorMode(ColorMode):
    @classmethod
    def get_name(self) -> str:
        return "Rotate"

    def __init__(self, child:ColorMode, angleDeg:float=45):
        if (child == None):
            raise ValueError("Child color mode unset")
        self.child = child
        self.angleRad = math.radians(angleDeg)
        self.center = Point(0.5, 0.5)

        corner = Point(0, 0)
        rotatedCorner = corner.rotateAround(self.center, self.angleRad)

        self.scale = 1
        if rotatedCorner.x < 0:
            self.scale = 0.5 / (0.5 - rotatedCorner.x)
        elif rotatedCorner.x > 1:
            self.scale = 0.5 / (0.5 - rotatedCorner.x) * -1
        elif rotatedCorner.y < 0:
            self.scale = 0.5 / (0.5 - rotatedCorner.y)
        elif rotatedCorner.y > 1:
            self.scale = 0.5 / (0.5 - rotatedCorner.y) * -1

    def getColor(self, x:float, y:float) -> FloatColor:
        transformedPoint = Point(x, y).rotateAround(self.center, self.angleRad)
        transformedPoint = (transformedPoint - self.center) * Point(self.scale, self.scale) + self.center
        return self.child.getColor(
            max(0, min(1, transformedPoint.x)),
            max(0, min(1, transformedPoint.y))
        )