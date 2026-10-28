from math import ceil, floor

from PySide6.QtGui import QPainter

from render import qcolor


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
