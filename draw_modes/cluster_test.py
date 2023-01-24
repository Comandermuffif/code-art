from __future__ import annotations

import cairo

from color_modes import ColorMode
from draw_modes import DrawMode
from models import Line, Point, Polygon

class ClusterTestDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Cluster (Test)"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'draw_edges': ("Draw Edges", bool, True),
            'draw_fill': ("Fill", bool, True),

            'top_line': ("Top Line", bool, False),
            'left_line': ("Left Line", bool, True),
            'bottom_line': ("Bottom Line", bool, True),
            'right_line': ("Right Line", bool, True),
        }

    def __init__(self, *args, **kwargs):
        self.draw_edges = kwargs["draw_edges"]
        self.draw_fill = kwargs["draw_fill"]

        self.top_line = kwargs["top_line"]
        self.left_line = kwargs["left_line"]
        self.bottom_line = kwargs["bottom_line"]
        self.right_line = kwargs["right_line"]

    def _draw_polygon(self, context:cairo.Context, color_mode:ColorMode, polygon:Polygon, width:int, height:int) -> None:
        context.move_to(*(polygon.points[0] * Point(width, height)).as_tuple())
        for point in polygon.points[1:]:
            context.line_to(*(point * Point(width, height)).as_tuple())
        context.close_path()

        color = color_mode.get_color(*(polygon.get_center() * Point(width, height)).as_tuple())

        if self.draw_fill and self.draw_edges:
            context.set_source_rgb(*color.to_tuple())
            context.fill_preserve()
            context.set_source_rgb(0, 0, 0)
            context.stroke()
        elif self.draw_fill:
            context.set_source_rgb(*color.to_tuple())
            context.fill()
        elif self.draw_edges:
            context.set_source_rgb(0, 0, 0)
            context.stroke()

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        boundary_lines = list[Line]()

        if self.top_line:
            boundary_lines.append(Line(Point(0.25, 0.25), Point(0.75, 0.25)).limit(1, 1))
        if self.bottom_line:
            boundary_lines.append(Line(Point(0.75, 0.75), Point(0.25, 0.75)).limit(1, 1))
        if self.left_line:
            boundary_lines.append(Line(Point(0.25, 0.25), Point(0.25, 0.75)).limit(1, 1))
        if self.right_line:
            boundary_lines.append(Line(Point(0.75, 0.75), Point(0.75, 0.25)).limit(1, 1))
        center = Point(0.5, 0.5)

        # Draw grey long lines
        for boundary_line in boundary_lines:
            context.move_to(*(boundary_line.point_a * Point(width, height)).as_tuple())
            context.line_to(*(boundary_line.point_b * Point(width, height)).as_tuple())
            context.set_source_rgb(0.5, 0.5, 0.5)
            context.stroke()

        # Draw polygon
        polygon = Polygon.from_segments(center, boundary_lines)
        self._draw_polygon(context, color_mode, polygon, width, height)