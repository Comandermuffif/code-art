import random
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class CirclesDrawMode(DrawMode):
    def __init__(self, count:int=500, minSize:int=0, maxSize:int=50):
        self.count = count
        self.minSize = minSize
        self.maxSize = maxSize

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        for _ in range(self.count):
            x = random.random()
            y = random.random()

            color = color_mode.getColor(x, y)

            x = x * width
            y = y * height

            radious = random.random() * (self.maxSize - self.minSize) + self.minSize

            context.set_source_rgba(*color.toTuple())
            context.arc(x, y, radious, 0, 360)
            context.fill()