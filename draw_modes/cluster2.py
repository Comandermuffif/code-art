from __future__ import annotations
import itertools

from math import atan2, cos, radians, sin

from random import random

import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import ColorPoint, FloatColor, Point
class Cluster2DrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Cluster2"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'points': ("Points", int, 5),
            'draw_centers': ("Draw Centers", bool, False),
        }

    def __init__(self, *args, **kwargs):
        self.points = [
            ColorPoint(random(), random(), None)
            for _ in range(int(kwargs["points"]))
        ]

        self.draw_centers = kwargs["draw_centers"]

        # self.points = [
        #     ColorPoint(0.51, 0.49, FloatColor(1, 0, 0)),
        #     ColorPoint(0.3, 0.3, FloatColor(0, 1, 0)),
        #     ColorPoint(0.75, 0.2, FloatColor(0, 0, 1)),
        # ]

    def _get_nearest_point(self, point:Point) -> tuple[ColorPoint, float]:
        distances = [
            (other_point, point.distance(other_point))
            for other_point in self.points
        ]

        distances = sorted(distances, key=lambda x: x[1])
        return distances[0]

    def _get_edge_points(self, point:Point, mid_point:Point, width:float, height:float) -> tuple[Point, Point, Point]:
        angle = atan2(mid_point.y - point.y, mid_point.x - point.x) + radians(90)

        offset = Point(cos(angle) * width, sin(angle) * height)

        left_point = mid_point - offset
        right_point = mid_point + offset

        # This needs to actually be the correct values

        # left_point.x = min(width, max(0, left_point.x))
        # left_point.y = min(height, max(0, left_point.y))

        # right_point.x = min(width, max(0, right_point.x))
        # right_point.y = min(height, max(0, right_point.y))

        return (left_point, right_point, mid_point)

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        corner_points = [
            Point(0, 0),
            Point(width, 0),
            Point(width, height),
            Point(0, height),
        ]

        # Assign colors and make points absolute
        for point in self.points:
            point.color = color_mode.get_color(point.x, point.y)
            point.x = point.x * width
            point.y = point.y * height

            # Draw each color point
            context.set_source_rgb(*point.color.to_tuple())
            context.arc(point.x, point.y, 20, 0, 360)
            context.fill()

        polygons = {
            p: list[Point]()
            for p in self.points
        }

        valid_trios = list[tuple[tuple[ColorPoint, ...], Point]]()

        for point_trio in itertools.combinations(self.points, 3):
            circumcenter = Point.get_circumcenter(*point_trio)
            distance = circumcenter.distance(point_trio[0])
            is_valid = True

            # The circumcenter is a true min if it's closest to the trio
            for other_point in self.points:
                # Skip trio points
                if other_point in point_trio:
                    continue

                other_dist = circumcenter.distance(other_point)
                if other_dist < distance:
                    is_valid = False
                    break

            if is_valid:
                valid_trios.append(
                    (point_trio, circumcenter)
                )
                context.set_source_rgb(0, 0, 0)
                context.arc(circumcenter.x, circumcenter.y, 5, 0, 360)
                context.fill()

                midpoint_a = Point.get_midpoint(point_trio[0], point_trio[1])
                midpoint_b = Point.get_midpoint(point_trio[1], point_trio[2])
                midpoint_c = Point.get_midpoint(point_trio[0], point_trio[2])

                # edge_points_a = self._get_edge_points(point_trio[0], midpoint_a, width, height)
                # edge_points_b = self._get_edge_points(point_trio[1], midpoint_b, width, height)
                # edge_points_c = self._get_edge_points(point_trio[2], midpoint_c, width, height)

                # Edge points are valid if they are the closest to that side

                # context.set_source_rgb(0.5, 0.5, 0.5)

                # for (edge_l, edge_r, midpoint) in [edge_points_a, edge_points_b, edge_points_c]:
                #     context.move_to(midpoint.x, midpoint.y)
                #     context.line_to(edge_l.x, edge_l.y)
                #     context.stroke()

                #     context.move_to(midpoint.x, midpoint.y)
                #     context.line_to(edge_r.x, edge_r.y)
                #     context.stroke()

                polygons[point_trio[0]].append(midpoint_a)
                polygons[point_trio[0]].append(midpoint_c)

                polygons[point_trio[1]].append(midpoint_a)
                polygons[point_trio[1]].append(midpoint_b)

                polygons[point_trio[2]].append(midpoint_b)
                polygons[point_trio[2]].append(midpoint_c)

                if distance < midpoint_b.distance(point_trio[0]):
                    polygons[point_trio[0]].append(circumcenter)
                else:
                    polygons[point_trio[0]].append(midpoint_b)

                if distance < midpoint_c.distance(point_trio[1]):
                    polygons[point_trio[1]].append(circumcenter)
                else:
                    polygons[point_trio[1]].append(midpoint_c)

                if distance < midpoint_a.distance(point_trio[2]):
                    polygons[point_trio[2]].append(circumcenter)
                else:
                    polygons[point_trio[2]].append(midpoint_a)

        for corner_point in corner_points:
            (nearest, distance) = self._get_nearest_point(corner_point)
            polygons[nearest].append(corner_point)

        for (point, polygon_points) in polygons.items():
            context.set_source_rgb(*point.color.to_tuple())

            # These need to be sorted
            sorted_p = sorted([
                (point.get_angle(p), p)
                for p in polygon_points
            ], key=lambda p: p[0])

            poly_p = [p[1] for p in sorted_p]

            context.move_to(poly_p[0].x, poly_p[0].y)
            for p_a in poly_p[1:]:
                context.line_to(p_a.x, p_a.y)

            context.close_path()
            context.fill()
            context.stroke()

        if self.draw_centers:
            for point in self.points:
                context.set_source_rgb(0, 0, 0)
                context.arc(point.x, point.y, 7, 0, 360)
                context.fill()
                context.set_source_rgb(*point.color.to_tuple())
                context.arc(point.x, point.y, 5, 0, 360)
                context.fill()