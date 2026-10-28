"""Linear gradient color mode: a smooth HSV rainbow across the canvas."""
import colorsys

from nodes.base import ColorMode, NodeDef

from models import FloatColor


class LinearGradientColorMode(ColorMode):
    def getColor(self, x: float, y: float) -> FloatColor:
        return FloatColor(*colorsys.hsv_to_rgb((x + y) * 0.5, 1, 1))


LINEAR_GRADIENT = NodeDef(
    title="Linear Gradient", category="Color",
    code='''@node_entry
def linear_gradient() -> "ColorMode":
    from nodes.color.linear_gradient import LinearGradientColorMode
    return LinearGradientColorMode()
''',
)
