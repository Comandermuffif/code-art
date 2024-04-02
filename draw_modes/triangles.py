import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class TrianglesDrawMode(DrawMode):
    def __init__(self, count:int=50):
        self.count = count

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        xStep = width / self.count
        yStep = width / self.count

        points = [
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1)
        ]

        offsets = [
            0.25,
            0.75,
        ]

        for xCount in range(self.count):
            for yCount in range(self.count):
                for offsetIndex in range(len(offsets)):
                    color = color_mode.getColor(
                        (xCount + offsets[offsetIndex])/self.count,
                        (yCount + offsets[offsetIndex])/self.count
                    )
                    context.set_source_rgba(*color.toTuple())

                    context.move_to((xCount + points[0 + offsetIndex][0]) * xStep, (yCount + points[0 + offsetIndex][1]) * yStep)
                    context.line_to((xCount + points[1 + offsetIndex][0]) * xStep, (yCount + points[1 + offsetIndex][1]) * yStep)
                    context.line_to((xCount + points[2 + offsetIndex][0]) * xStep, (yCount + points[2 + offsetIndex][1]) * yStep)
                    context.close_path()
                    context.fill_preserve()
                    context.stroke()