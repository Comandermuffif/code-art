"""Qt (QPainter) rendering for code-art.

Port of the old cairo draw modes onto PySide6. Each draw_* function has the
signature:

    def draw_x(painter: QPainter, color_mode, width: int, height: int, **params) -> None

where `color_mode` is any object exposing ``getColor(x, y) -> FloatColor`` with
x, y in [0, 1]. Use :func:`render_to_qimage` to produce a QImage from a color
mode plus one of these draw functions.
"""
from __future__ import annotations

from PySide6.QtGui import QImage, QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPointF

from models import FloatColor


def qcolor(color: FloatColor) -> QColor:
    """Convert a FloatColor (r/g/b/a floats in 0..1) to a QColor."""
    return QColor.fromRgbF(color.r, color.g, color.b, color.a)


def render_to_qimage(
    color_mode,
    draw_func,
    width: int,
    height: int,
    background: tuple[float, float, float, float] = (0, 0, 0, 0),
    **params,
) -> QImage:
    """Render `color_mode` with `draw_func` into a new QImage of w x h.

    `background` is an r/g/b/a tuple in 0..1 used to fill the canvas first
    (default fully transparent).
    """
    image = QImage(width, height, QImage.Format.Format_ARGB32)
    image.fill(QColor.fromRgbF(*background))

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    try:
        draw_func(painter, color_mode, width, height, **params)
    finally:
        painter.end()
    return image
