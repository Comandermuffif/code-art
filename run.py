from math import cos, radians, sin

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from color_modes import ColorMode
from color_modes.arc import ArcColorMode
from color_modes.modify.normal import NormalColorMode
from color_modes.polygon import PolygonColorMode
from color_modes.random import RandomColorMode
from draw_modes import DrawMode, toQColor
from draw_modes.circles import CirclesDrawMode
from draw_modes.squares import SquaresDrawMode
from models import FloatColor
from random import shuffle


class PathDrawMode(DrawMode):
    def __init__(self, points:list[tuple[float, float]]):
        self.points = points

    def draw(self, painter:QPainter, colorMode:ColorMode):
        width = painter.viewport().width()
        height = painter.viewport().height()
        
        path = QPainterPath()
        path.moveTo(self.points[0][0] * width, self.points[0][1] * height)
        for point in self.points:
            path.lineTo(point[0] * width, point[1] * height)
        path.closeSubpath()

        pen = QPen(toQColor(FloatColor(0, 0, 0)), 5)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.strokePath(path, pen)


def genCirclePoints(center:tuple[float,float], radious:float, segments=20) -> list[tuple[float, float]]:
    return list([
        (
            center[0] + cos(radians(360 * (float(x)/segments))) * radious,
            center[1] + sin(radians(360 * (float(x)/segments))) * radious
        ) for x in range(segments)
    ])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Code Art"
        self.setWindowTitle(self.title)

        # Create the canvas
        canvas = QImage(1024, 1024, QImage.Format.Format_ARGB32_Premultiplied)
        canvas.fill(Qt.GlobalColor.transparent)

        # Create the painter
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create our color pallete
        pallete = FloatColor.fromHexList("#eaac43,#ea4c65,#1a2431,#57a37d,#cace9d,#527157,#ff0000,#ffa500,#ffff00,#008000,#0000ff,#4b0082,#ee82ee,#02d7f2,#f2e900,#007aff,#ff1111,#000000,#ffbe0b,#fb5607,#ff006e,#8338ec,#3a86ff")
        shuffle(pallete)
        pallete = pallete[0:3]
        # pallete = FloatColor.fromHexList("#eaac43,#ea4c65,#1a2431,#57a37d,#cace9d,#527157")
        pallete = FloatColor.getSubcolors(pallete, 7, True)

        # Draw our content
        SquaresDrawMode(1).draw(painter, RandomColorMode([FloatColor(1, 1, 1, 1)]), 1024, 1024)
        CirclesDrawMode().draw(painter, PolygonColorMode([
                (FloatColor(0, 0, 0, 0), [(0.3, 1.0), (0.7, 1.0), (0.5, 0.5)]),
                (NormalColorMode(ArcColorMode(pallete), 0.0, 0.0), genCirclePoints((0.5, 0.5), 0.45)),
            ]),
            1024,
            1024,
        )

        # Create a widget so we can view it
        painter.end()
        image = QPixmap.fromImage(canvas)
        label = QLabel()

        # Add to window
        label.setPixmap(image)
        self.setCentralWidget(label)
        self.resize(image.width(), image.height())


if __name__ == '__main__':
    # Create basic window
    app = QApplication([])
    window = MainWindow()

    # Show window
    window.show()
    app.exec()
