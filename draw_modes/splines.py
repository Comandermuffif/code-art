import math
import random
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class SpinesDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Splines"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),

            'min_length': ("Min Length", int, 0),
            'max_length': ("Max Length", int, 50),

            'min_width': ("Min Width", int, 5),
            'max_width': ("Max Width", int, 5),

            'min_angle': ("Min Angle", int, -30),
            'max_angle': ("Max Angle", int, 30),

            'min_start_angle': ("Min Start Angle", int, 0),
            'max_start_angle': ("Max Start Angle", int, 360),

            'chain_count': ("Chains", int, 2),
        }

    def __init__(self, *args, **kwargs):
        self.count = int(kwargs["count"])
        self.min_length = int(kwargs["min_length"])
        self.max_length = int(kwargs["max_length"])
        self.min_width = int(kwargs["min_width"])
        self.max_width = int(kwargs["max_width"])
        self.min_angle = int(kwargs["min_angle"])
        self.max_angle = int(kwargs["max_angle"])
        self.min_start_angle = int(kwargs["min_start_angle"])
        self.max_start_angle = int(kwargs["max_start_angle"])
        self.chain_count = int(kwargs["chain_count"])

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        for _ in range(self.count):

            x = random.randint(0, width)
            y = random.randint(0, height)
            context.move_to(x, y)

            length = random.random() * (self.max_length - self.min_length) + self.min_length
            angle = math.radians(random.random() * (self.max_start_angle - self.min_start_angle) + self.min_start_angle)

            for _ in range(self.chain_count + 1):
                color = color_mode.get_color(x/width, y/height)
                context.set_source_rgb(color.r, color.g, color.b)

                line_width = random.random() * (self.max_width - self.min_width) + self.min_width
                context.set_line_width(line_width)

                next_x = x + math.cos(angle) * length
                next_y = y + math.sin(angle) * length

                context.line_to(next_x, next_y)

                x = next_x
                y = next_y
                angle = angle + math.radians(random.random() * (self.max_angle - self.min_angle) + self.min_angle)

            context.stroke()