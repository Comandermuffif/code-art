"""Transform modifier: offset, scale, and rotate a child color mode."""
import math

from nodes.base import ColorMode, NodeDef, Widget

from models import FloatColor, Point


class TransformColorMode(ColorMode):
    center = Point(0.5, 0.5)

    def __init__(self, child: ColorMode, xOffset: float = 0, yOffset: float = 0, xScale: float = 1, yScale: float = 1, angleDeg: float = 0):
        if (child == None):
            raise ValueError("Child color mode unset")
        self.child = child
        self.angleRad = math.radians(angleDeg)

        self.offset = Point(xOffset, yOffset)
        self.scale = Point(xScale, yScale)

    def getColor(self, x: float, y: float) -> FloatColor:
        newPoint = Point(x, y) - self.offset

        delta = newPoint - self.center
        delta = delta / self.scale

        newPoint = self.center + delta
        newPoint = newPoint.rotateAround(self.center, -1 * self.angleRad)

        if newPoint.x < 0 or newPoint.x > 1 or newPoint.y < 0 or newPoint.y > 1:
            return FloatColor(0, 0, 0, 0)  # Clear

        return self.child.getColor(newPoint.x, newPoint.y)


TRANSFORM = NodeDef(
    title="Transform", category="Color Modifier",
    code='''@node_entry
def transform(child: ColorMode = None, x_offset: float = 0, y_offset: float = 0, x_scale: float = 1, y_scale: float = 1, angle_deg: float = 0) -> ColorMode:
    from nodes.modify.transform import TransformColorMode
    return TransformColorMode(child, x_offset, y_offset, x_scale, y_scale, angle_deg)
''',
    widgets=[
        Widget("x_offset", "float", 0.0, -1.0, 1.0),
        Widget("y_offset", "float", 0.0, -1.0, 1.0),
        Widget("x_scale", "float", 1.0, 0.0, 4.0),
        Widget("y_scale", "float", 1.0, 0.0, 4.0),
        Widget("angle_deg", "float", 0.0, -360.0, 360.0),
    ],
)
