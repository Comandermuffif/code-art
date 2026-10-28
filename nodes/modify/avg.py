"""Average modifier: blend several color modes by averaging their colors."""
from nodes.base import ColorMode, NodeDef

from models import FloatColor


class AvgColorMode(ColorMode):
    def __init__(self, *colorModes: ColorMode):

        for colorMode in colorModes:
            if (colorMode == None):
                raise ValueError("Color mode unset")

        self.colorModes = colorModes

    def getColor(self, x: float, y: float) -> FloatColor:
        return sum([
            colorMode.getColor(x, y)
            for colorMode in self.colorModes
        ], FloatColor(0, 0, 0)) * (1 / len(self.colorModes))


AVG = NodeDef(
    title="Average", category="Color Modifier",
    code='''@node_entry
def avg(a: "ColorMode" = None, b: "ColorMode" = None) -> "ColorMode":
    from nodes.modify.avg import AvgColorMode
    return AvgColorMode(a, b)
''',
)
