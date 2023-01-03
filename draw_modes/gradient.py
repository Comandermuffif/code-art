import math
import random
import cairo

from draw_modes import DrawMode
from models import FloatColor

class GradientDrawMode(DrawMode):
    def get_name(cls):
        return "Gradient"

    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'max_size': ("Max Size", int, 50),
            'subcount': ("Subcount", int, 2),
        }

    def draw(self, context:cairo.Context, colors:list[FloatColor], *args, **kwargs):
        subcount = int(kwargs["subcount"])
        full_colors = GradientDrawMode.get_subcolors(colors, subcount)

        for _ in range(int(kwargs["count"])):
            x_float = random.random()
            y_float = random.random()

            color_index = math.floor((x_float + y_float)/2 * len(full_colors))
            color = full_colors[color_index]
            context.set_source_rgb(color.r, color.g, color.b)

            x = x_float * int(kwargs["width"])
            y = y_float * int(kwargs["height"])

            radious = random.randint(0, int(kwargs["max_size"]))
            context.arc(x, y, radious, 0, 360)
            context.fill()

    def __str__(self) -> str:
        return self.get_name()

    @classmethod
    def get_subcolors(cls, colors:list[FloatColor], subcount:int) -> list[FloatColor]:
        full_colors = list()

        for i in range(len(colors) - 1):
            current_color = colors[i]
            full_colors.append(current_color)

            next_color = colors[i + 1]

            color_delta = next_color - current_color

            for j in range(subcount):
                full_colors.append(current_color + (color_delta * ((j + 1) / (subcount + 1))))

        full_colors.append(colors[-1])

        return full_colors

