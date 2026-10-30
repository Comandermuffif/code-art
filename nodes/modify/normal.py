"""Normal modifier: jitter sample coordinates by a normal distribution."""
import random

from nodes.base import ColorMode, NodeDef, Widget

from models import FloatColor


class NormalColorMode(ColorMode):
    def __init__(self, child: ColorMode, xDivergance: float = 0.1, yDivergance: float = 0.1):
        if (child == None):
            raise ValueError("Child color mode unset")
        self.child = child
        self.xDivergance = xDivergance
        self.yDivergance = yDivergance

    def getColor(self, x: float, y: float) -> FloatColor:
        return self.child.getColor(
            x + random.normalvariate(0, self.xDivergance),
            y + random.normalvariate(0, self.yDivergance)
        )


NORMAL = NodeDef(
    title="Normal", category="Color Modifier",
    code='''@node_entry
def normal(child: ColorMode = None, x_divergence: float = 0.1, y_divergence: float = 0.1) -> ColorMode:
    from nodes.modify.normal import NormalColorMode
    return NormalColorMode(child, x_divergence, y_divergence)
''',
    widgets=[
        Widget("x_divergence", "float", 0.1, 0.0, 1.0),
        Widget("y_divergence", "float", 0.1, 0.0, 1.0),
    ],
)
