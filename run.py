from math import cos, radians, sin

from PySide6.QtCore import QPointF, Qt, QVariantAnimation
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget

from color_modes import ColorMode
from color_modes.arc import ArcColorMode
from color_modes.gradient import GradientColorMode
from color_modes.modify.normal import NormalColorMode
from color_modes.polygon import PolygonColorMode
from color_modes.random import RandomColorMode
from draw_modes import DrawMode, toQColor
from draw_modes.circles import CirclesDrawMode
from draw_modes.squares import SquaresDrawMode
from models import FloatColor
from random import randint, random, shuffle


class Circle():
    def __init__(self, colorMode:ColorMode):
        self.x = random()
        self.y = random()
        self.color = toQColor(colorMode.getColor(self.x, self.y))

        self.minRadious = 10
        self.maxRadious = 50
        self.radious = random() * (self.maxRadious - self.minRadious) + self.minRadious

    def draw(self, painter: QPainter) -> None:
        width = painter.window().width()
        height = painter.window().height()

        painter.setBrush(self.color)
        painter.drawEllipse(QPointF(self.x * width, self.y * height), self.radious, self.radious)


class WiggleCircle(Circle):
    def __init__(self, colorMode:ColorMode):
        super().__init__(colorMode)
        self.xOrigin = self.x
        self.yOrigin = self.y

        self.xOffset = 0
        self.yOffset = 0

        self.maxOffset = 0.05

        moveSpeed = 0.001
        self.xSpeed = random() * moveSpeed - (moveSpeed/2)
        self.ySpeed = random() * moveSpeed - (moveSpeed/2)

    def draw(self, painter: QPainter) -> None:
        self.xOffset += self.xSpeed
        self.yOffset += self.ySpeed

        self.x = self.xOrigin + self.xOffset
        self.y = self.yOrigin + self.yOffset

        if abs(self.xOffset) > self.maxOffset:
            self.xSpeed *= -1
        if abs(self.yOffset) > self.maxOffset:
            self.ySpeed *= -1

        super().draw(painter)


class ArcWidget(QWidget):
    def __init__(self):
        super().__init__()

        colorMode = GradientColorMode(FloatColor.getSubcolors(FloatColor.fromHexList("#eaac43,#ea4c65,#1a2431,#57a37d,#cace9d,#527157"), 7, True))

        self.circles = list([
            WiggleCircle(colorMode) for _ in range(1000)
        ])

        self.anim = QVariantAnimation(self, duration=1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(360)
        self.anim.valueChanged.connect(self.update)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)

        for c in self.circles:
            c.draw(painter)

        if self.anim.currentValue() == self.anim.endValue():
            self.anim.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("AnimateArc")
        self.setGeometry(100, 100, 600, 600)
        self.arcWidget = ArcWidget()
        self.setCentralWidget(self.arcWidget)


if __name__ == '__main__':
    # Create basic window
    app = QApplication([])
    window = MainWindow()

    # Show window
    window.show()
    app.exec()
