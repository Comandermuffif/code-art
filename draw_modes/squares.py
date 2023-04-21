from math import ceil, floor
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class SquaresDrawMode(DrawMode):
    def __init__(self, count:int=50):
        self.count = count

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        x_step = width/self.count
        y_step = height/self.count

        for count_x in range(self.count):
            for count_y in range(self.count):
                color = color_mode.getColor(count_x/self.count, count_y/self.count)

                context.set_source_rgba(*color.toTuple())
                context.rectangle(floor(count_x * x_step), floor(count_y * y_step), ceil(x_step), ceil(y_step))
                context.fill()