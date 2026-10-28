import random

from scipy.spatial import Voronoi

from PySide6.QtGui import QPainter, QPen, QPolygonF
from PySide6.QtCore import QPointF

from render import qcolor


def draw_voronoi(
    painter: QPainter,
    color_mode,
    width: int,
    height: int,
    count: int = 300,
) -> None:
    points = [(random.random(), random.random()) for _ in range(count)]

    # Add points so we don't have to figure out non-enclosed regions.
    points.append((-4, -4))
    points.append((4, -4))
    points.append((4, 4))
    points.append((-4, 4))

    voronoi = Voronoi(points)

    region_points = {
        voronoi.point_region[index]: voronoi.points[index]
        for index in range(len(voronoi.point_region))
    }

    for region_index in range(len(voronoi.regions)):
        region = voronoi.regions[region_index]

        # Skip unclosed and empty regions.
        if -1 in region:
            continue
        if len(region) == 0:
            continue

        polygon = QPolygonF([
            QPointF(voronoi.vertices[p][0] * width, voronoi.vertices[p][1] * height)
            for p in region
        ])

        point = region_points[region_index]
        color = qcolor(color_mode.getColor(point[0], point[1]))

        painter.setBrush(color)
        painter.setPen(QPen(color, 1))
        painter.drawPolygon(polygon)
