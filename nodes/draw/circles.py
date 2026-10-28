"""Circles draw mode: scatter randomly placed, randomly sized circles."""
import random

from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF

from nodes.base import NodeDef, Widget
from nodes.draw._render import qcolor, render_to_qimage


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


DRAW_CIRCLES = NodeDef(
    title="Draw Circles", category="Draw",
    code='''@node_entry
def circles(field: "ColorMode" = None, count: int = 300, min_size: float = 2, max_size: float = 20, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from nodes.draw._render import render_to_qimage
    from nodes.draw.circles import draw_circles
    return render_to_qimage(field, draw_circles, width, height, count=count, min_size=min_size, max_size=max_size)
''',
    widgets=[
        Widget("count", "int", 300, 1, 5000),
        Widget("min_size", "float", 2.0, 0.0, 200.0),
        Widget("max_size", "float", 20.0, 0.0, 200.0),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)
