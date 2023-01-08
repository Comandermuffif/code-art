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
            'subcount': ("Subcount", int, 2),
            'divergance': ("Divergance", float, 0),
        }

    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        self.subcount = int(kwargs["subcount"])
        self.divergance = float(kwargs["divergance"])
        self.full_colors = self.get_subcolors(colors, self.subcount)

    def get_color(self, x:float, y:float) -> FloatColor:
        buckets = len(self.full_colors)
        bucket_width = 2/buckets
        color_prob = []

        for i in range(buckets):
            color_prob.append(None)

        for i in range(buckets):
            color_prob[i] = abs(random.normalvariate(bucket_width * (i + 0.5), self.divergance) - (x + y))

        max_prob = min(color_prob)
        for i in range(buckets):
            if max_prob == color_prob[i]:
                return self.full_colors[i]
        return (0, 0, 0)

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