import random
import cairo

from draw_modes import DrawMode
from models import FloatColor
from utils.bucketed import BucketedUtils

class BucketedDrawMode(DrawMode):
    max_distance = 2

    def get_name(cls):
        return "Bucketed"

    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'max_size': ("Max Size", int, 50),
            'divergance': ("Divergance", float, 0),
        }

    def draw(self, context:cairo.Context, colors:list[FloatColor], *args, **kwargs):
        divergance = float(kwargs["divergance"])

        for _ in range(int(kwargs["count"])):
            x_float = random.random()
            y_float = random.random()

            color = BucketedUtils.get_color(x_float, y_float, colors, divergance)
            context.set_source_rgb(color.r, color.g, color.b)

            x = x_float * int(kwargs["width"])
            y = y_float * int(kwargs["height"])

            radious = random.randint(0, int(kwargs["max_size"]))
            context.arc(x, y, radious, 0, 360)
            context.fill()

    def __str__(self) -> str:
        return self.get_name()