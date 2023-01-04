import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class SquaresDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Squares"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 50),
        }

    def __init__(self, *args, **kwargs):
        self.count = int(kwargs["count"])

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        x_step = width/self.count
        y_step = height/self.count

        for count_x in range(self.count):
            for count_y in range(self.count):
                color = color_mode.get_color(count_x/self.count, count_y/self.count)

                context.set_source_rgb(color.r, color.g, color.b)
                context.rectangle(count_x * x_step, count_y * y_step, x_step, y_step)
                context.fill()