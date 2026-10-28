"""Squares draw mode: a grid of filled squares."""
from math import ceil, floor

from PySide6.QtGui import QPainter

from nodes.base import NodeDef, Widget
from nodes.draw._render import qcolor, render_to_qimage


def draw_squares(
    painter: QPainter,
    color_mode,
    width: int,
    height: int,
    count: int = 50,
) -> None:
    x_step = width / count
    y_step = height / count

    for count_x in range(count):
        for count_y in range(count):
            color = qcolor(color_mode.getColor(count_x / count, count_y / count))
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(
                floor(count_x * x_step),
                floor(count_y * y_step),
                ceil(x_step),
                ceil(y_step),
            )


DRAW_SQUARES = NodeDef(
    title="Draw Squares", category="Draw",
    code='''@node_entry
def squares(field: ColorMode = None, count: int = 30, width: int = 512, height: int = 512) -> QImage:
    """@outputs: image"""
    from nodes.draw._render import render_to_qimage
    from nodes.draw.squares import draw_squares
    return render_to_qimage(field, draw_squares, width, height, count=count)
''',
    widgets=[
        Widget("count", "int", 30, 1, 500),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)
