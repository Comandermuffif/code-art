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
        # Sample coordinates are only nominally in [0, 1]: modifier nodes such as
        # Normal jitter them with a normal distribution, so the computed index can
        # land outside [0, buckets). Clamp rather than index blindly -- an index
        # above buckets raises IndexError and a negative one silently wraps around
        # to the end of the palette.
        index = max(0, min(index, buckets - 1))
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
