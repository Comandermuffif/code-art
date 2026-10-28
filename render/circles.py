import random

from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF

from render import qcolor


def draw_circles(
    painter: QPainter,
    color_mode,
    width: int,
    height: int,
    count: int = 500,
    min_size: float = 0,
    max_size: float = 50,
) -> None:
    for _ in range(count):
        x = random.random()
        y = random.random()

        color = qcolor(color_mode.getColor(x, y))

        px = x * width
        py = y * height
        radious = random.random() * (max_size - min_size) + min_size

        painter.setBrush(color)
        painter.setPen(color)
        painter.drawEllipse(QPointF(px, py), radious, radious)
