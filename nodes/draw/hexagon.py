"""Hexagon draw mode: a tiling of hexagons around the canvas center."""
import math

from PySide6.QtGui import QPainter, QPen, QPolygonF
from PySide6.QtCore import QPointF

from models import Point
from nodes.base import NodeDef, Widget
from nodes.draw._render import qcolor, render_to_qimage


def _translate(offset: Point) -> Point:
    return Point(
        math.cos(math.radians(30)) * offset.x,
        -math.sin(math.radians(30)) * offset.x + offset.y,
    )


def draw_hexagon(
    painter: QPainter,
    color_mode,
    width: int,
    height: int,
    count: int = 50,
    radious: float = 0.8,
) -> None:
    origin = Point(0.5, 0.5) * Point(width, height)
    scale = Point(width / count, height / count)

    sides = 6
    local_points = [
        Point(
            math.cos(math.radians(360 * (i / sides))) * radious * 0.58,
            math.sin(math.radians(360 * (i / sides))) * radious * 0.58,
        )
        for i in range(sides)
    ]

    for x_offset in range(-count, count):
        for y_offset in range(-count, count):
            offset = Point(x_offset, y_offset)

            hex_center = origin + _translate(offset) * scale
            if hex_center.x < -scale.x or hex_center.x > width + scale.x:
                continue
            if hex_center.y < -scale.y or hex_center.y > height + scale.y:
                continue

            translated_points = [
                origin + (local_point + _translate(offset)) * scale
                for local_point in local_points
            ]

            polygon = QPolygonF([QPointF(p.x, p.y) for p in translated_points])

            center = Point(0.5, 0.5) + offset / scale
            color = qcolor(color_mode.getColor(*center.as_tuple()))

            painter.setBrush(color)
            painter.setPen(QPen(color, 1))
            painter.drawPolygon(polygon)


DRAW_HEXAGON = NodeDef(
    title="Draw Hexagon", category="Draw",
    code='''@node_entry
def hexagon(field: "ColorMode" = None, count: int = 12, radious: float = 0.8, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from nodes.draw._render import render_to_qimage
    from nodes.draw.hexagon import draw_hexagon
    return render_to_qimage(field, draw_hexagon, width, height, count=count, radious=radious)
''',
    widgets=[
        Widget("count", "int", 12, 1, 100),
        Widget("radious", "float", 0.8, 0.0, 2.0),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)
