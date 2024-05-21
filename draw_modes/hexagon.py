from math import ceil, floor
import math
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import Point

class HexagonDrawMode(DrawMode):
    def __init__(self, count:int=50, radious=0.45):
        self.origin = Point(0.5, 0.5)
        self.count = count

        sides = 6
        self.localPoints = [
            Point(
                math.cos(math.radians(360 * (i / sides))) * radious,
                math.sin(math.radians(360 * (i / sides))) * radious
            ) + Point(0.5, 0.5)
            for i in range(sides)
        ]

    def _getHexPoints(self, offset:Point) -> list[Point]:
        return list([
            p + self._translate(offset)
            for p in self.localPoints
        ])
    
    @staticmethod
    def _translate(offset:Point) -> Point:
        return Point(
                math.cos(math.radians(30)) * offset.x,
                -math.sin(math.radians(30)) * offset.x + offset.y,
            )

    def _drawHexagon(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int, offset:Point) -> None:
        origin = self.origin * Point(width, height)
        scale = Point(width/self.count, height/self.count)

        hexCenter = origin + self._translate(offset) * scale
        if hexCenter.x < -scale.x or hexCenter.x > width + scale.x:
            return
        if hexCenter.y < -scale.y or hexCenter.y > height + scale.y:
            return

        # Convert shape points into pixel coordinates
        translatedPoints = list([
            origin + (p * scale)
            for p in self._getHexPoints(offset)
        ])

        # Start at the first point
        context.move_to(*translatedPoints[0].as_tuple())

        # Line to every other point
        for point in translatedPoints[1:]:
            context.line_to(*point.as_tuple())

        # Close the shape
        context.close_path()

        # Fill
        center = self.origin + offset/scale
        context.set_source_rgba(*color_mode.getColor(*center.as_tuple()).toTuple())
        context.fill()

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        # Draw the center hexagon
        for xOffset in range(-self.count, self.count):
            for yOffset in range(-self.count, self.count):
                self._drawHexagon(context, color_mode, width, height, Point(xOffset, yOffset))