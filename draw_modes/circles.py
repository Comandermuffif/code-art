import random

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter

from color_modes import ColorMode
from draw_modes import DrawMode, toQColor

class CirclesDrawMode(DrawMode):
    def __init__(self, count:int=500, minSize:int=0, maxSize:int=50):
        self.count = count
        self.minSize = minSize
        self.maxSize = maxSize

    def draw(self, painter:QPainter, color_mode:ColorMode, width:int, height:int) -> None:
        painter.setPen(Qt.PenStyle.NoPen)

        for _ in range(self.count):
            x = random.random()
            y = random.random()

            color = color_mode.getColor(x, y)

            x = x * width
            y = y * height

            radious = random.random() * (self.maxSize - self.minSize) + self.minSize

            painter.setBrush(toQColor(color))
            painter.drawEllipse(QPointF(x, y), radious, radious)