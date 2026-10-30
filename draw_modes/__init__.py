from abc import abstractmethod

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen

from color_modes import ColorMode
from models import FloatColor

def toQColor(color:FloatColor) -> QColor:
    r, g, b, a = color.toTuple()
    return QColor.fromRgbF(min(max(r, 0.0), 1.0), min(max(g, 0.0), 1.0), min(max(b, 0.0), 1.0), min(max(a, 0.0), 1.0))

def strokePen(color:FloatColor) -> QPen:
    # Matches cairo's defaults: 1px wide, flat caps, miter joins
    pen = QPen(toQColor(color), 1.0)
    pen.setCapStyle(Qt.PenCapStyle.FlatCap)
    pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
    return pen

def fillAndStroke(painter:QPainter, path:QPainterPath, color:FloatColor) -> None:
    painter.fillPath(path, toQColor(color))
    painter.setPen(strokePen(color))
    painter.drawPath(path)

class DrawMode(object):
    @abstractmethod
    def draw(self, painter:QPainter, colorMode:ColorMode, width:int, height:int) -> None:
        pass