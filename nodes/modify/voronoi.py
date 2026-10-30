"""Voronoi modifier: quantize a child color mode onto random cell centers."""
from random import random
from scipy.spatial import Voronoi, cKDTree

from nodes.base import ColorMode, NodeDef, Widget

from models import FloatColor


class VoronoiColorMode(ColorMode):
    def __init__(self, child: ColorMode, count: int = 10):
        self.child = child

        points = [
            (random(), random())
            for _ in range(count)
        ]

        # Add points so we don't have to figure out non-enclosed regions
        points.append((-4, -4))
        points.append((4, -4))
        points.append((4, 4))
        points.append((-4, 4))

        self.voronoi = Voronoi(points)
        self.tree = cKDTree(points)

    def getColor(self, x: float, y: float) -> FloatColor:
        test_point_dist, test_point_region = self.tree.query([[x, y]])
        (p_x, p_y) = self.tree.data[test_point_region[0]]
        return self.child.getColor(p_x, p_y)


VORONOI = NodeDef(
    title="Voronoi", category="Color Modifier",
    code='''@node_entry
def voronoi(child: ColorMode = None, count: int = 10) -> ColorMode:
    from nodes.modify.voronoi import VoronoiColorMode
    return VoronoiColorMode(child, count)
''',
    widgets=[Widget("count", "int", 10, 1, 200)],
)
