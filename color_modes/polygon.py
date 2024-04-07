from scipy.spatial import Delaunay

from color_modes import ColorMode
from models import FloatColor, Point

class PolygonColorMode(ColorMode):
    def __init__(self, polygons:list[tuple[ColorMode|FloatColor, list[tuple[float, float]]]]):
        self.polygons:list[tuple[ColorMode|FloatColor, Delaunay]] = []

        for (color, points) in polygons:
            hull = Delaunay(points)
            hull.close()
            self.polygons.append((color, hull))

    def scaleToFit(self, hull:Delaunay, x:float, y:float) -> tuple[float, float]:
        newX = hull.min_bound[0] + x * (hull.max_bound[0] - hull.min_bound[0])
        newY = hull.min_bound[1] + y * (hull.max_bound[1] - hull.min_bound[1])
        return (newX, newY)

    def invertFit(self, hull:Delaunay, x:float, y:float) -> tuple[float, float]:
        newX = (x - hull.min_bound[0]) / (hull.max_bound[0] - hull.min_bound[0])
        newY = (y - hull.min_bound[1]) / (hull.max_bound[1] - hull.min_bound[1])
        return (newX, newY)

    def getColor(self, x:float, y:float) -> FloatColor:
        for (child, hull) in self.polygons:
            if hull.find_simplex((x, y)) >= 0:
                if isinstance(child, ColorMode):

                    x, y = self.invertFit(hull, x, y)

                    return child.getColor(x, y)
                return child
        return FloatColor(0, 0, 0, 0)
