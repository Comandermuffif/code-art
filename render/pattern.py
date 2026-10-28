from PySide6.QtGui import QPainter, QPen, QPolygonF
from PySide6.QtCore import QPointF

from models import Point
from render import qcolor


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
