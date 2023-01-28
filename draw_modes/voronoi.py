import cairo

from random import random
from scipy.spatial import Voronoi

from color_modes import ColorMode
from draw_modes import DrawMode

class VoronoiDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Voronoi"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 3000),
        }

    def __init__(self, *args, **kwargs):
        self.count = kwargs["count"]

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:

        points = [
            (random(), random())
            for _ in range(self.count)
        ]

        # Add points so we don't have to figure out non-enclosed regions
        points.append((-width*4, -height*4))
        points.append((width*4, -height*4))
        points.append((width*4, height*4))
        points.append((-width*4, height*4))

        voronoi = Voronoi(points)

        region_points = {
            voronoi.point_region[index]: voronoi.points[index]
            for index in range(len(voronoi.point_region))
        }

        # For every region
        # for region in voronoi.regions:
        for region_index in range(len(voronoi.regions)):
            region = voronoi.regions[region_index]
            # If it is a closed region
            if -1 in region:
                continue

            # Skip empty regions
            if len(region) == 0:
                continue

            # Move to the first point
            vertex = voronoi.vertices[region[0]]
            context.move_to(vertex[0] * width, vertex[1] * height)

            for point_index in region[1:]:
                vertex = voronoi.vertices[point_index]
                # Draw a line to every other point
                context.line_to(vertex[0] * width, vertex[1] * height)

            context.close_path()

            # Get the point for the region
            point = region_points[region_index]
            color = color_mode.get_color(point[0], point[1])
            context.set_source_rgb(color.r, color.g, color.b)
            context.stroke_preserve()
            context.fill()