import math
import random
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class LinesDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Lines"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'min_length': ("Min Length", int, 0),
            'max_length': ("Max Length", int, 50),
            'min_width': ("Min Width", int, 3),
            'max_width': ("Max Width", int, 10),
            'min_angle': ("Min Angle", int, 0),
            'max_angle': ("Max Angle", int, 360),
        }

    def __init__(self, *args, **kwargs):
        self.count = int(kwargs["count"])
        self.min_length = int(kwargs["min_length"])
        self.max_length = int(kwargs["max_length"])
        self.min_width = int(kwargs["min_width"])
        self.max_width = int(kwargs["max_width"])
        self.min_angle = int(kwargs["min_angle"])
        self.max_angle = int(kwargs["max_angle"])

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        for _ in range(self.count):
            x = random.random()
            y = random.random()

            color = color_mode.get_color(x, y)

            x = x * width
            y = y * height

            length = random.random() * (self.max_length - self.min_length) + self.min_length
            angle = math.radians(random.random() * (self.max_angle - self.min_angle) + self.min_angle)

            context.set_source_rgb(color.r, color.g, color.b)

            line_width = random.random() * (self.max_width - self.min_width) + self.min_width
            context.set_line_width(line_width)

            context.move_to(x + math.cos(angle) * (length / 2), y + math.sin(angle) * (length / 2))
            context.line_to(x + math.cos(angle) * -(length / 2), y + math.sin(angle) * -(length / 2))
            context.stroke()