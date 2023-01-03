import random
import cairo

from draw_modes import DrawMode
from models import FloatColor

class RandomDrawMode(DrawMode):
    def get_name(cls):
        return "Random"

    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'max_size': ("Max Size", int, 50),
        }

    def draw(self, context:cairo.Context, colors:list[FloatColor], *args, **kwargs):

        for _ in range(int(kwargs["count"])):
            x = random.randint(0, int(kwargs["width"]))
            y = random.randint(0, int(kwargs["height"]))

            color = random.choice(colors)
            context.set_source_rgb(color.r, color.g, color.b)

            radious = random.randint(0, int(kwargs["max_size"]))
            context.arc(x, y, radious, 0, 360)
            context.fill()

    def __str__(self) -> str:
        return self.get_name()

