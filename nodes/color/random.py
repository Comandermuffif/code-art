"""Random color mode: a random palette color per sample."""
import random

from nodes.base import ColorMode, NodeDef, Widget

from models import FloatColor


class RandomColorMode(ColorMode):
    def __init__(self, colors: list[FloatColor]):
        self.colors = colors

    def getColor(self, x: float, y: float) -> FloatColor:
        return random.choice(self.colors)


RANDOM = NodeDef(
    title="Random", category="Color",
    code='''@node_entry
def random(colors: str = "#ff0000,#00ff00,#0000ff") -> ColorMode:
    from models import FloatColor
    from nodes.color.random import RandomColorMode
    return RandomColorMode(FloatColor.fromHexList(colors))
''',
    widgets=[Widget("colors", "text", "#ff0000,#00ff00,#0000ff")],
)
