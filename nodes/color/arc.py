"""Arc color mode: palette colors swept around the center by angle."""
import math

from nodes.base import ColorMode, NodeDef, Widget

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
def arc(colors: str = "#ff0000,#00ff00,#0000ff,#ffff00,#00ffff") -> ColorMode:
    from models import FloatColor
    from nodes.color.arc import ArcColorMode
    return ArcColorMode(FloatColor.fromHexList(colors))
''',
    widgets=[Widget("colors", "text", "#ff0000,#00ff00,#0000ff,#ffff00,#00ffff")],
)
