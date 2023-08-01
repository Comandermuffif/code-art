import cairo

from random import random
from scipy.spatial import Voronoi

from color_modes import ColorMode
from draw_modes import DrawMode

class VoronoiDrawMode(DrawMode):
    def __init__(self, count:int=3000):
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

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        region_points = {
            self.voronoi.point_region[index]: self.voronoi.points[index]
            for index in range(len(self.voronoi.point_region))
        }

        # For every region
        # for region in self.voronoi.regions:
        for region_index in range(len(self.voronoi.regions)):
            region = self.voronoi.regions[region_index]
            # If it is a closed region
            if -1 in region:
                continue

            # Skip empty regions
            if len(region) == 0:
                continue

            # Move to the first point
            vertex = self.voronoi.vertices[region[0]]
            context.move_to(vertex[0] * width, vertex[1] * height)

            for point_index in region[1:]:
                vertex = self.voronoi.vertices[point_index]
                # Draw a line to every other point
                context.line_to(vertex[0] * width, vertex[1] * height)

            context.close_path()

            # Get the point for the region
            point = region_points[region_index]
            color = color_mode.getColor(point[0], point[1])
            context.set_source_rgba(*color.toTuple())
            context.stroke_preserve()
            context.fill()