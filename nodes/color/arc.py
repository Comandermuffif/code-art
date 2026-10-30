"""Arc color mode: palette colors swept around the center by angle."""
import math

from nodes.base import ColorMode, NodeDef

from models import FloatColor, Point


class ArcColorMode(ColorMode):
    def __init__(self, colors: list[FloatColor]):
        self.center = Point(0.5, 0.5)
        self.colors = list(colors)

    def getColor(self, x: float, y: float) -> FloatColor:
        angle = math.degrees(math.atan2(y - self.center.y, x - self.center.x))
        return self.colors[math.floor(len(self.colors) * angle / 360)]


ARC = NodeDef(
    title="Arc", category="Color",
    code='''@node_entry
def arc(colors: list[FloatColor] = None) -> ColorMode:
    from nodes.color.arc import ArcColorMode
    if colors is None:
        raise ValueError("Arc: no color palette connected")
    return ArcColorMode(colors)
''',
)
