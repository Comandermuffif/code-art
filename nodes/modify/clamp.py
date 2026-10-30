"""Clamp modifier: harden a child color mode's alpha at a threshold."""
from nodes.base import ColorMode, NodeDef, Widget

from models import FloatColor


class ClampColorMode(ColorMode):
    def __init__(self, child: ColorMode, threshold: float = 0.5):
        self.child = child
        self.theshold = threshold

    def getColor(self, x: float, y: float) -> FloatColor:
        orig = self.child.getColor(x, y)
        orig.a = 1 if orig.a >= self.theshold else 0
        return orig


CLAMP = NodeDef(
    title="Clamp", category="Color Modifier",
    code='''@node_entry
def clamp(child: ColorMode = None, threshold: float = 0.5) -> ColorMode:
    from nodes.modify.clamp import ClampColorMode
    return ClampColorMode(child, threshold)
''',
    widgets=[Widget("threshold", "float", 0.5, 0.0, 1.0)],
)
