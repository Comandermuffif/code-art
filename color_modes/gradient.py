import math
import random

from color_modes import ColorMode
from models import FloatColor

class GradientColorMode(ColorMode):
    @classmethod
    def get_name(self) -> str:
        return "Gradient"

    @classmethod
    def get_option_types(self) -> dict[str, tuple[str, type, object]]:
        return {
            'angle': ("Angle (Deg)", float, 45),
            'subcount': ("Subcount", int, 2),
            'divergance': ("Divergance", float, 0),
        }

    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        self.angle = float(kwargs["angle"])
        self.subcount = int(kwargs["subcount"])
        self.divergance = float(kwargs["divergance"])
        self.full_colors = FloatColor.get_subcolors(colors, self.subcount)

        self._weight_x = math.cos(math.radians(self.angle)) * math.sqrt(2)
        self._weight_y = math.sin(math.radians(self.angle)) * math.sqrt(2)

    def get_color(self, x:float, y:float) -> FloatColor:
        buckets = len(self.full_colors)

        weight_x = abs(self._weight_x)
        weight_y = abs(self._weight_y)

        max_width = weight_x + weight_y
        bucket_width = max_width/buckets

        if self._weight_x < 0:
            x = (x - 0.5) * -1 + 0.5

        if self._weight_y < 0:
            y = (y - 0.5) * -1 + 0.5

        color_prob = [
            abs(random.normalvariate(bucket_width * (i + 0.5), self.divergance) - (x * weight_x + y * weight_y))
            for i in range(buckets)
        ]

        max_prob = min(color_prob)
        for i in range(buckets):
            if max_prob == color_prob[i]:
                return self.full_colors[i]
        return (0, 0, 0)