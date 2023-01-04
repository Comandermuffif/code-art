import math
import random
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class CirclesDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Circles"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'min_size': ("Min Size", int, 0),
            'max_size': ("Max Size", int, 50),
        }

    def __init__(self, *args, **kwargs):
        self.count = int(kwargs["count"])
        self.min_size = int(kwargs["min_size"])
        self.max_size = int(kwargs["max_size"])

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        for _ in range(self.count):
            x = random.random()
            y = random.random()

            color = color_mode.get_color(x, y)

            x = x * width
            y = y * height

            radious = random.random() * (self.max_size - self.min_size) + self.min_size

            context.set_source_rgb(color.r, color.g, color.b)
            context.arc(x, y, radious, 0, 360)
            context.fill()