from __future__ import annotations

from random import random

import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import ColorPoint, Point, Rect

class Cluster3DrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Cluster3"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'points': ("Points", int, 5),
            'resolution': ("Resolution", int, 10),
            'draw_centers': ("Draw Centers", bool, False),
        }

    def __init__(self, *args, **kwargs):
        self.points = [
            ColorPoint(random(), random(), None)
            for _ in range(int(kwargs["points"]))
        ]

        self.resolution = kwargs["resolution"]
        self.draw_centers = kwargs["draw_centers"]

    def _get_nearest_point(self, point:Point) -> tuple[ColorPoint, float]:
        distances = [
            (other_point, point.distance(other_point))
            for other_point in self.points
            if other_point != point
        ]

        distances = sorted(distances, key=lambda x: x[1])
        return distances[0]

    def _rect_colors(self, rect:Rect) -> list[ColorPoint]:
        found_colors = set[ColorPoint]()
        for corner_point in rect.corner_points():
            nearest_point = self._get_nearest_point(corner_point)
            found_colors.add(nearest_point[0])

        return found_colors

    def _draw_rect(self, context:cairo.Context, rect:Rect):
        available_colors = self._rect_colors(rect)
        color_count = len(available_colors)

        if rect.width < self.resolution or rect.height < self.resolution:
            context.set_source_rgb(*available_colors.pop().color.to_tuple())
            context.rectangle(rect.x, rect.y, rect.width, rect.height)
            context.fill()
            return

        if color_count == 1:
            context.set_source_rgb(*available_colors.pop().color.to_tuple())
            context.rectangle(rect.x, rect.y, rect.width, rect.height)
            context.fill()
        elif color_count > 0:
            for sub_rect in rect.subdivide():
                self._draw_rect(context, sub_rect)
        else:
            context.set_source_rgb(1, 1, 1)
            context.rectangle(rect.x, rect.y, rect.width, rect.height)
            context.fill()

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        # Assign colors and make points absolute
        for point in self.points:
            point.color = color_mode.get_color(point.x, point.y)
            point.x = point.x * width
            point.y = point.y * height

        start_rect = Rect(0, 0, width, height)
        self._draw_rect(context, start_rect)

        if self.draw_centers:
            for point in self.points:
                context.set_source_rgb(0, 0, 0)
                context.arc(point.x, point.y, 7, 0, 360)
                context.fill()
                context.set_source_rgb(*point.color.to_tuple())
                context.arc(point.x, point.y, 5, 0, 360)
                context.fill()