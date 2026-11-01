from math import ceil, floor

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter

from color_modes import ColorMode
from draw_modes import DrawMode, toQColor

class SquaresDrawMode(DrawMode):
    def __init__(self, count:int=50):
        self.count = count

    def draw(self, painter:QPainter, color_mode:ColorMode, width:int, height:int) -> None:
        x_step = width/self.count
        y_step = height/self.count

        painter.setPen(Qt.PenStyle.NoPen)

        for count_x in range(self.count):
            for count_y in range(self.count):
                color = color_mode.getColor(count_x/self.count, count_y/self.count)

                painter.setBrush(toQColor(color))
                painter.drawRect(QRectF(floor(count_x * x_step), floor(count_y * y_step), ceil(x_step), ceil(y_step)))