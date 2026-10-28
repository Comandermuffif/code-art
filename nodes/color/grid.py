"""Grid color mode: a palette laid out as a color grid."""
import math

from nodes.base import ColorMode, NodeDef, Widget

from models import FloatColor


class GridColorMode(ColorMode):
    def __init__(self, colors: list[FloatColor]):
        self.colors = colors
        self.side = int(math.sqrt(len(self.colors)))

    def getColor(self, x: float, y: float) -> FloatColor:
        index = math.floor(x * self.side) + math.floor(y * (self.side + 1)) * self.side
        if index >= len(self.colors):
            index = -1
        return self.colors[index]


GRID = NodeDef(
    title="Grid", category="Color",
    code='''@node_entry
def grid(colors: str = "#ff0000,#00ff00,#0000ff,#ffff00") -> "ColorMode":
    from models import FloatColor
    from nodes.color.grid import GridColorMode
    return GridColorMode(FloatColor.fromHexList(colors))
''',
    widgets=[Widget("colors", "text", "#ff0000,#00ff00,#0000ff,#ffff00")],
)
