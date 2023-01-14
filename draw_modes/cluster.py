from math import sqrt

from random import choice, random

import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import FloatColor

class ClusterDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Cluster"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'points': ("Points", int, 5),
        }

    def __init__(self, *args, **kwargs):
        self.points = [
            (random(), random())
            for _ in range(int(kwargs["points"]))
        ]

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:

        points = [
            {
                'point': point,
                'color': color_mode.get_color(*point),
            }
            for point in self.points
        ]

        for pixel_x in range(width):
            for pixel_y in range(height):

                color = self.get_nearest_point(pixel_x/width, pixel_y/height, points)

                context.set_source_rgb(color.r, color.g, color.b)
                context.rectangle(pixel_x, pixel_y, 1, 1)
                context.fill()

    @classmethod
    def get_nearest_point(cls, x:float, y:float, points:list[dict]) -> FloatColor:
        distances = [
            {
                'distance': cls._get_distance((x, y), (point_pair['point'])),
                'color': point_pair['color']
            }
            for point_pair in points
        ]

        distances = sorted(distances, key=lambda x: x['distance'])

        return distances[0]['color']

    @classmethod
    def _get_distance(cls, point_a:tuple[float, float], point_b:tuple[float, float]) -> float:
        return sqrt(pow(point_a[0] - point_b[0], 2) + pow(point_a[1] - point_b[1], 2))