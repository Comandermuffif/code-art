"""Pattern draw mode: stamp a polygon shape across a grid."""
from PySide6.QtGui import QPainter, QPen, QPolygonF
from PySide6.QtCore import QPointF

from models import Point
from nodes.base import NodeDef, Widget
from nodes.draw._render import qcolor, render_to_qimage


def draw_pattern(
    painter: QPainter,
    color_mode,
    width: int,
    height: int,
    points: list[tuple[float, float]],
    count: int = 50,
) -> None:
    x_step = width / count
    y_step = height / count

    center = sum([Point(p[0], p[1]) for p in points], Point(0, 0)) * (1 / len(points))

    for x_count in range(count):
        for y_count in range(count):
            color = qcolor(color_mode.getColor(
                (x_count + center.x) / count,
                (y_count + center.y) / count,
            ))

            polygon = QPolygonF([
                QPointF((x_count + p[0]) * x_step, (y_count + p[1]) * y_step)
                for p in points
            ])

            painter.setBrush(color)
            painter.setPen(QPen(color, 1))
            painter.drawPolygon(polygon)


DRAW_PATTERN = NodeDef(
    title="Draw Pattern", category="Draw",
    code='''@node_entry
def pattern(field: ColorMode = None, points: str = "0,0;1,0;0.5,1", count: int = 12, width: int = 512, height: int = 512) -> QImage:
    """@outputs: image"""
    from nodes.draw._render import render_to_qimage
    from nodes.draw.pattern import draw_pattern
    pts = [tuple(float(v) for v in pair.split(',')) for pair in points.split(';')]
    return render_to_qimage(field, draw_pattern, width, height, points=pts, count=count)
''',
    widgets=[
        Widget("points", "text", "0,0;1,0;0.5,1"),
        Widget("count", "int", 12, 1, 200),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)
