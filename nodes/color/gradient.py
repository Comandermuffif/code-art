"""Gradient color mode: a banded linear gradient over a color palette."""
import math

from nodes.base import ColorMode, NodeDef, Widget

from models import FloatColor


class GradientColorMode(ColorMode):
    orientations = [
        (1, 1),
        (1, 0),
        (0, 1),
    ]
    scales = [2, 1, 1]

    def __init__(self, colors: list[FloatColor], orientation: int = 0):
        self.colors = colors
        self.weights = self.orientations[orientation]
        self.scale = self.scales[orientation]

    def getColor(self, x: float, y: float) -> FloatColor:
        buckets = len(self.colors)
        index = math.floor((x * buckets * self.weights[0] + y * buckets * self.weights[1]) / self.scale)
        if (index == buckets):
            return self.colors[-1]
        return self.colors[index]


GRADIENT = NodeDef(
    title="Gradient", category="Color",
    code='''@node_entry
def gradient(colors: list[FloatColor] = None, orientation: int = 0) -> ColorMode:
    from nodes.color.gradient import GradientColorMode
    if colors is None:
        raise ValueError("Gradient: no color palette connected")
    return GradientColorMode(colors, orientation)
''',
    widgets=[Widget("orientation", "int", 0, 0, 2)],
)
