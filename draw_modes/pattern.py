import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import Point

class PatternDrawMode(DrawMode):
    def __init__(self, points:list[tuple[float,float]], count:int=50):
        self.points = points
        self.count = count
        self.center:Point = sum([Point(p[0], p[1]) for p in points], Point(0, 0)) * (1/len(points))

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        xStep = width / self.count
        yStep = width / self.count

        for xCount in range(self.count):
            for yCount in range(self.count):
                color = color_mode.getColor(
                    (xCount + self.center.x)/self.count,
                    (yCount + self.center.y)/self.count
                )
                context.set_source_rgba(*color.toTuple())

                for pointIndex in range(len(self.points)):
                    if pointIndex == 0:
                        context.move_to((xCount + self.points[pointIndex][0]) * xStep, (yCount + self.points[pointIndex][1]) * yStep)
                    else:
                        context.line_to((xCount + self.points[pointIndex][0]) * xStep, (yCount + self.points[pointIndex][1]) * yStep)
                context.close_path()
                context.fill_preserve()
                context.stroke()