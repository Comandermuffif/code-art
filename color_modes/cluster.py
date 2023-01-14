from math import pow, sqrt
from random import normalvariate, choice, random

from color_modes import ColorMode
from models import FloatColor

class ClusterColorMode(ColorMode):
    @classmethod
    def get_name(cls) -> str:
        return "Cluster"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'subcount': ("Subcount", int, 2),
            'points': ("Points", int, 10),
            'divergance': ("Divergance", float, 0),
        }

    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        self.subcount = int(kwargs["subcount"])
        self.divergance = float(kwargs["divergance"])
        full_colors = self.get_subcolors(colors, self.subcount)

        self.color_points = [
            (random(), random(), choice(full_colors))
            for _ in range(int(kwargs["points"]))
        ]

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

    @classmethod
    def _get_distance(cls, point_a:tuple[float, float], point_b:tuple[float, float]) -> float:
        return sqrt(pow(point_a[0] - point_b[0], 2) + pow(point_a[1] - point_b[1], 2))

    def get_color(self, x:float, y:float) -> FloatColor:
        current_point = (x, y)

        distances = [
            (self._get_distance(current_point, color_point[:2]), color_point[2])
            for color_point in self.color_points
        ]

        sorted_distances = sorted(distances, key=lambda a : a[0])

        if self.divergance > 0:
            divergant_color = FloatColor(normalvariate(0, self.divergance), normalvariate(0, self.divergance), normalvariate(0, self.divergance))
            return sorted_distances[0][1] + divergant_color
        else:
            return sorted_distances[0][1]
        # index = distances.index(sorted_distances[1])
        # next_nearest_color = self.colors[index]

        # ratio = sorted_distances[0] / (sorted_distances[0] + sorted_distances[1])

        # return nearest_color * (1 - ratio) + next_nearest_color * ratio