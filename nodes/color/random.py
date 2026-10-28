"""Random color mode: a random palette color per sample."""
import random

from nodes.base import ColorMode, NodeDef

from models import FloatColor


class RandomColorMode(ColorMode):
    def __init__(self, colors: list[FloatColor]):
        self.colors = colors

    def getColor(self, x: float, y: float) -> FloatColor:
        return random.choice(self.colors)


RANDOM = NodeDef(
    title="Random", category="Color",
    code='''@node_entry
def random(colors: list[FloatColor] = None) -> ColorMode:
    from nodes.color.random import RandomColorMode
    if colors is None:
        raise ValueError("Random: no color palette connected")
    return RandomColorMode(colors)
''',
)
