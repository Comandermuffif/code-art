import math
from color_modes import ColorMode
from models import FloatColor, Point

class TransformColorMode(ColorMode):
    @classmethod
    def get_name(self) -> str:
        return "Transform"

    def __init__(self, child:ColorMode, xOffset:float=0, yOffset:float=0, xScale:float=1, yScale:float=1, angleDeg:float=45):
        if (child == None):
            raise ValueError("Child color mode unset")
        self.child = child
        self.angleRad = math.radians(angleDeg)
        self.center = Point(0.5, 0.5)

        corner = Point(0, 0)
        rotatedCorner = corner.rotateAround(self.center, self.angleRad)

        self.angleScale = 1
        if rotatedCorner.x < 0:
            self.angleScale = 0.5 / (0.5 - rotatedCorner.x)
        elif rotatedCorner.x > 1:
            self.angleScale = 0.5 / (0.5 - rotatedCorner.x) * -1
        elif rotatedCorner.y < 0:
            self.angleScale = 0.5 / (0.5 - rotatedCorner.y)
        elif rotatedCorner.y > 1:
            self.angleScale = 0.5 / (0.5 - rotatedCorner.y) * -1

        self.offset = Point(xOffset, yOffset)
        self.scale = Point(xScale, yScale)

    def getColor(self, x:float, y:float) -> FloatColor:
        # Rotate
        transformedPoint = Point(x, y).rotateAround(self.center, self.angleRad)
        transformedPoint = (transformedPoint - self.center) * Point(self.angleScale, self.angleScale) + self.center

        # Scale
        transformedPoint = transformedPoint * self.scale

        # Translate
        transformedPoint = transformedPoint + self.offset

        if transformedPoint.x < 0 or transformedPoint.x > 1 or transformedPoint.y < 0 or transformedPoint.y > 1:
            return FloatColor(0, 0, 0, 0)
        return self.child.getColor(transformedPoint.x,transformedPoint.y)