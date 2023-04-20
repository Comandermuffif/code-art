import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class TrianglesDrawMode(DrawMode):
    def __init__(self, count=50):
        self.count = count

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        step = width/self.count

        points_a = [
            (0, 0),
            (1, 0),
            (0.5, 1),
        ]
        center_a = (sum([x[0] for x in points_a])/len(points_a), sum([x[1] for x in points_a])/len(points_a))

        points_b = [
            (1, 0),
            (1.5, 1),
            (0.5, 1),
        ]
        center_b = (sum([x[0] for x in points_b])/len(points_b), sum([x[1] for x in points_b])/len(points_b))

        for count_x in range(self.count):
            for count_y in range(self.count):

                if count_y % 2 == 0:
                    color = color_mode.getColor((count_x + center_a[0])/self.count, (count_y + center_a[1])/self.count)
                    context.set_source_rgb(color.r, color.g, color.b)

                    context.move_to((count_x + points_a[0][0]) * step, (count_y + points_a[0][1]) * step)
                    context.line_to((count_x + points_a[1][0]) * step, (count_y + points_a[1][1]) * step)
                    context.line_to((count_x + points_a[2][0]) * step, (count_y + points_a[2][1]) * step)
                    context.close_path()
                    context.fill_preserve()
                    context.stroke()

                    color = color_mode.getColor((count_x + center_b[0])/self.count, (count_y + center_b[1])/self.count)
                    context.set_source_rgb(color.r, color.g, color.b)

                    context.move_to((count_x + points_b[0][0]) * step, (count_y + points_b[0][1]) * step)
                    context.line_to((count_x + points_b[1][0]) * step, (count_y + points_b[1][1]) * step)
                    context.line_to((count_x + points_b[2][0]) * step, (count_y + points_b[2][1]) * step)
                    context.close_path()
                    context.fill_preserve()
                    context.stroke()
                else:
                    color = color_mode.getColor((count_x + center_a[0])/self.count, (count_y + center_a[1])/self.count)
                    context.set_source_rgb(color.r, color.g, color.b)

                    context.move_to((count_x + points_a[0][0]) * step, (count_y + 1 - points_a[0][1]) * step)
                    context.line_to((count_x + points_a[1][0]) * step, (count_y + 1 - points_a[1][1]) * step)
                    context.line_to((count_x + points_a[2][0]) * step, (count_y + 1 - points_a[2][1]) * step)
                    context.close_path()
                    context.fill_preserve()
                    context.stroke()

                    color = color_mode.getColor((count_x + center_b[0])/self.count, (count_y + center_b[1])/self.count)
                    context.set_source_rgb(color.r, color.g, color.b)

                    context.move_to((count_x + points_b[0][0]) * step, (count_y + 1 - points_b[0][1]) * step)
                    context.line_to((count_x + points_b[1][0]) * step, (count_y + 1 - points_b[1][1]) * step)
                    context.line_to((count_x + points_b[2][0]) * step, (count_y + 1 - points_b[2][1]) * step)
                    context.close_path()
                    context.fill_preserve()
                    context.stroke()