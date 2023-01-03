import math
import random
import cairo

from draw_modes import DrawMode
from models import FloatColor

class BucketedDrawMode(DrawMode):
    max_distance = 2

    def get_name(cls):
        return "Bucketed"

    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'max_size': ("Max Size", int, 50),
        }

    def draw(self, context:cairo.Context, colors:list[FloatColor], *args, **kwargs):
        for _ in range(int(kwargs["count"])):
            x_float = random.random()
            y_float = random.random()

            color_index = math.floor((x_float + y_float)/2 * len(colors))

            color = colors[color_index]
            context.set_source_rgb(color.r, color.g, color.b)

            x = x_float * int(kwargs["width"])
            y = y_float * int(kwargs["height"])

            radious = random.randint(0, int(kwargs["max_size"]))
            context.arc(x, y, radious, 0, 360)
            context.fill()

    def __str__(self) -> str:
        return self.get_name()

class BucketedRandomDrawMode(DrawMode):
    max_distance = 2

    def get_name(cls):
        return "Bucketed (Random)"

    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'max_size': ("Max Size", int, 50),
            'divergance': ("Divergance", float, 0.15),
        }

    def draw(self, context:cairo.Context, colors:list[FloatColor], *args, **kwargs):
        divergance = float(kwargs["divergance"])

        for _ in range(int(kwargs["count"])):
            x_float = random.random()
            y_float = random.random()

            color = BucketedRandomDrawMode._get_color(x_float, y_float, colors, divergance)
            context.set_source_rgb(color.r, color.g, color.b)

            x = x_float * int(kwargs["width"])
            y = y_float * int(kwargs["height"])

            radious = random.randint(0, int(kwargs["max_size"]))
            context.arc(x, y, radious, 0, 360)
            context.fill()

    def __str__(self) -> str:
        return self.get_name()

    @classmethod
    def _get_color(cls, x:float, y:float, colors:list[FloatColor], divergance:float):
        buckets = len(colors)
        bucket_width = cls.max_distance/buckets
        color_prob = []

        for i in range(buckets):
            color_prob.append(None)

        for i in range(buckets):
            color_prob[i] = abs(random.normalvariate(bucket_width * (i + 0.5), divergance) - (x + y))

        max_prob = min(color_prob)
        for i in range(buckets):
            if max_prob == color_prob[i]:
                return colors[i]
        return (0, 0, 0)

