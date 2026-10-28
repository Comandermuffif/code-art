"""Triangles draw mode: a grid of interlocking filled triangles."""
from PySide6.QtGui import QPainter, QPen, QPolygonF
from PySide6.QtCore import QPointF

from nodes.base import NodeDef, Widget
from nodes.draw._render import qcolor, render_to_qimage


def draw_triangles(
    painter: QPainter,
    color_mode,
    width: int,
    height: int,
    count: int = 50,
) -> None:
    x_step = width / count
    y_step = height / count

    points = [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
    ]

    offsets = [
        0.25,
        0.75,
    ]

    for x_count in range(count):
        for y_count in range(count):
            for offset_index in range(len(offsets)):
                color = qcolor(color_mode.getColor(
                    (x_count + offsets[offset_index]) / count,
                    (y_count + offsets[offset_index]) / count,
                ))

                triangle = QPolygonF([
                    QPointF((x_count + points[0 + offset_index][0]) * x_step, (y_count + points[0 + offset_index][1]) * y_step),
                    QPointF((x_count + points[1 + offset_index][0]) * x_step, (y_count + points[1 + offset_index][1]) * y_step),
                    QPointF((x_count + points[2 + offset_index][0]) * x_step, (y_count + points[2 + offset_index][1]) * y_step),
                ])

                painter.setBrush(color)
                painter.setPen(QPen(color, 1))
                painter.drawPolygon(triangle)


DRAW_TRIANGLES = NodeDef(
    title="Draw Triangles", category="Draw",
    code='''@node_entry
def triangles(field: ColorMode = None, count: int = 30, width: int = 512, height: int = 512) -> QImage:
    """@outputs: image"""
    from nodes.draw._render import render_to_qimage
    from nodes.draw.triangles import draw_triangles
    return render_to_qimage(field, draw_triangles, width, height, count=count)
''',
    widgets=[
        Widget("count", "int", 30, 1, 300),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)
