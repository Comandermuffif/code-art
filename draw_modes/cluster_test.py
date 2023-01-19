from __future__ import annotations
import itertools
import logging

from random import choice, random

import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import ColorPoint, Line, LineSegment, Point

class ClusterTestDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Cluster (Test)"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 1000),
            'centers': ("Centers", int, 50),
            'draw_centers': ("Draw Centers", bool, True),
            'draw_lines': ("Draw Lines", bool, True),
        }

    def __init__(self, *args, **kwargs):
        self.points = [
            Point(0.31234, 0.312341),
            # Point(0.51234, 0.512346),
            Point(0.2168764, 0.7653416),
            Point(0.86512, 0.396846),
        ]

        # self.points = [
        #     Point(random(), random())
        #     for _ in range(kwargs["centers"])
        # ]

        self.count = kwargs["count"]
        self.draw_centers = kwargs["draw_centers"]
        self.draw_lines = kwargs["draw_lines"]

    @classmethod
    def reduce(cls, center:Point, boundaries:list[Line]) -> list[LineSegment]:
        pass

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        points = [
            ColorPoint(p.x * width, p.y * height, color_mode.get_color(p.x, p.y))
            for p in self.points
        ]

        unreduced_polygons = dict[Point, list[Line]]()
        decision_lines = list[tuple[Line, ColorPoint, ColorPoint]]()

        for (point_a, point_b) in itertools.combinations(points, 2):
            line = Line.get_decision_boundary(point_a, point_b)
            decision_lines.append((line, point_a, point_b))

            if point_a not in unreduced_polygons:
                unreduced_polygons[point_a] = list[Line]()
            if point_b not in unreduced_polygons:
                unreduced_polygons[point_b] = list[Line]()

            unreduced_polygons[point_a].append(line)
            unreduced_polygons[point_b].append(line)

        # Draw black decision lines
        if self.draw_lines:
            for (decision_line, point_a, point_b) in decision_line:
                context.move_to(0, line.get_y(0))
                context.line_to(width, line.get_y(width))
                context.set_source_rgb(0, 0, 0)
                context.stroke()

        # Draw red intersection lines
        for (line_a, line_b) in itertools.combinations([decision_line for (decision_line, point_a, point_b) in decision_lines], 2):
            intersection = line_a.get_intersection(line_b)
            context.set_source_rgb(1, 0, 0)
            context.arc(intersection.x, intersection.y, 7, 0, 360)
            context.fill()

        # for _ in range(self.count):
        #     point = Point(random() * width, random() * height)

        #     possible_colors = set(points)

        #     for (decision_line, point_a, point_b) in decision_lines:

        #         if point_a not in possible_colors or point_b not in possible_colors:
        #             continue

        #         if decision_line.get_side(point) < 0:
        #             possible_colors.remove(point_b)
        #         else:
        #             possible_colors.remove(point_a)

        #         if len(possible_colors) < 2:
        #             break

        #     nearest_point = possible_colors.pop()
        #     context.set_source_rgb(*nearest_point.color.to_tuple())
        #     context.arc(point.x, point.y, 5, 0, 360)
        #     context.fill()

        # Draw colored centers
        if self.draw_centers:
            for point in points:
                context.set_source_rgb(0, 0, 0)
                context.arc(point.x, point.y, 7, 0, 360)
                context.fill()
                context.set_source_rgb(*point.color.to_tuple())
                context.arc(point.x, point.y, 5, 0, 360)
                context.fill()