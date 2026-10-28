"""Invert modifier: negate a child color mode's RGB."""
from nodes.base import ColorMode, NodeDef

from models import FloatColor


class InvertColorMode(ColorMode):
    def __init__(self, child: ColorMode):
        self.child = child

    def getColor(self, x: float, y: float) -> FloatColor:
        orig = self.child.getColor(x, y)
        return FloatColor(1 - orig.r, 1 - orig.g, 1 - orig.b)


INVERT = NodeDef(
    title="Invert", category="Color Modifier",
    code='''@node_entry
def invert(child: "ColorMode" = None) -> "ColorMode":
    from nodes.modify.invert import InvertColorMode
    return InvertColorMode(child)
''',
)
