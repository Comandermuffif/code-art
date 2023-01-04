import math
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class OverlappingCirclesDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Overlapping Circles"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 10),
        }

    def __init__(self, *args, **kwargs):
        self.count = int(kwargs["count"])

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        center_x = width/2
        center_y = height/2

        max_radious = math.sqrt(math.pow(center_x, 2) + math.pow(center_y, 2))

        for step in range(self.count):
            ratio = step/self.count

            color = color_mode.get_color(ratio, ratio)

            radious = max_radious * (1 - ratio)

            context.set_source_rgb(color.r, color.g, color.b)
            context.arc(center_x, center_y, radious, 0, 360)
            context.fill()