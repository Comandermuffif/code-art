from __future__ import annotations
import itertools
import logging

from math import atan2, cos, radians, sin

from random import random

import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import ColorPoint, FloatColor, Line, LineSegment, Point, Polygon
class SmartClusterDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Smart Cluster"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 5),
            'draw_centers': ("Draw Centers", bool, True),
            'draw_edges': ("Draw Edges", bool, True),
            'draw_fill': ("Fill", bool, True),
        }

    def __init__(self, *args, **kwargs):
        self.count = kwargs["count"]
        self.draw_centers = kwargs["draw_centers"]
        self.draw_edges = kwargs["draw_edges"]
        self.draw_fill = kwargs["draw_fill"]

    def _draw_polygon(self, context:cairo.Context, center:ColorPoint, polygon:Polygon, width:int, height:int) -> None:
        logging.debug(f"Starting polygon {center.color}")

        for point in polygon.points:
            if point == polygon.points[0]:
                context.move_to(*(point * Point(width, height)).as_tuple())
            else:
                context.line_to(*(point * Point(width, height)).as_tuple())

            logging.debug(f"Adding point {point}")
        context.close_path()

        if self.draw_fill and self.draw_edges:
            context.set_source_rgb(*center.color.to_tuple())
            context.fill_preserve()
            context.set_source_rgb(0, 0, 0)
            context.stroke()
        elif self.draw_fill:
            context.set_source_rgb(*center.color.to_tuple())
            context.fill()
        elif self.draw_edges:
            context.set_source_rgb(0, 0, 0)
            context.stroke()

    def _draw_center(self, context:cairo.Context, color_point:ColorPoint, width:int, height:int) -> None:
        context.set_source_rgb(0, 0, 0)
        context.arc(color_point.x * width, color_point.y * height, 7, 0, 360)
        context.fill()
        context.set_source_rgb(*color_point.color.to_tuple())
        context.arc(color_point.x * width, color_point.y * height, 5, 0, 360)
        context.fill()

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:

        points = list[ColorPoint]()
        for _ in range(self.count):
            x = random()
            y = random()
            points.append(ColorPoint(x, y, color_mode.get_color(x, y)))

        # points = [
        #     ColorPoint(0.3, 0.2, FloatColor(1, 0, 0)),
        #     ColorPoint(0.8, 0.45, FloatColor(0, 1, 0)),
        #     ColorPoint(0.25, 0.75, FloatColor(0, 0, 1)),
        # ]

        decision_lines = dict[ColorPoint, list[LineSegment]]()

        for (p1, p2) in itertools.combinations(points, 2):
            line = Line.get_decision_boundary(p1, p2).limit(1, 1)

            if p1 not in decision_lines:
                decision_lines[p1] = []
            if p2 not in decision_lines:
                decision_lines[p2] = []

            decision_lines[p1].append(line)
            decision_lines[p2].append(line)

            if self.draw_edges:
                context.move_to(*(line.point_a * Point(width, height)).as_tuple())
                context.line_to(*(line.point_b * Point(width, height)).as_tuple())
                context.set_source_rgb(0.5, 0.5, 0.5)
                context.stroke()
                logging.debug(f"Drawing {line}")

        for (p, lines) in decision_lines.items():
            polygon = Polygon.from_segments(p, lines)
            # The blue polygon is has one line that is being reduced to a single point in the reduction step
            self._draw_polygon(context, p, polygon, width, height)

        if self.draw_centers:
            for point in points:
                self._draw_center(context, point, width, height)
