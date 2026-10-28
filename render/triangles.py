from PySide6.QtGui import QPainter, QPen, QPolygonF
from PySide6.QtCore import QPointF

from render import qcolor


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
