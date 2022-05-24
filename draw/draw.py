"""Draw

Usage:
  draw.py [options] circle <max-size> <count>
  draw.py [options] triangle <count>

Options:
  -h --help                   Show this screen
  -W --width <px>             The width of the image to create in pixels [default: 2048]
  -H --height <px>            The height of the image to create in pixels [default: 2048]

  --rainbow                   Use a rainbow pattern for coloring
  --greyscale                 Rainbow but with only greyscale
  --circle                    Raidiate from the center

"""
import docopt
import cairo
import colorsys
import math
import random
import string

class FromCenterColor(object):
  max_distance = math.sqrt(math.pow(-0.5, 2) + math.pow(-0.5, 2))

  def __init__(self, divergance=0.35):
    self.divergance = divergance

  def get_color(self, x:float, y:float):
    distance_from_center = math.sqrt(math.pow(x-0.5, 2) + math.pow(y-0.5, 2))
    hue = distance_from_center/FromCenterColor.max_distance
    return colorsys.hsv_to_rgb(hue * random.gauss(1, self.divergance), 1, 1)

class FromTopLeftColor(object):
  max_distance = math.sqrt(2)

  def __init__(self, divergance=0.35):
    self.divergance = divergance

  def get_color(self, x:float, y:float):
    distance_from_corner = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    hue = distance_from_corner/FromTopLeftColor.max_distance
    return colorsys.hsv_to_rgb(hue * random.gauss(1, self.divergance), 1, 1)

def draw_circles(surface:cairo.ImageSurface, color_class:object,  max_size:float, count:int):
  context = cairo.Context(surface)
  width = surface.get_width()
  height = surface.get_height()
  context.set_line_width(1)
  for _ in range(count):
    x = random.random()
    y = random.random()
    size = random.random() * max_size
    context.set_source_rgb(*color_class.get_color(x, y))
    context.arc(x * width, y * height, size, 0, 360)
    context.fill()

def draw_triangles(surface:cairo.ImageSurface, color_func,  count:int):
  context = cairo.Context(surface)
  width = surface.get_width()
  height = surface.get_height()
  context.set_line_width(1)
  x_step = width/count
  y_step = height/count
  points = [
    (0, 0),
    (0, 1),
    (1, 1),
    (1, 0)
  ]

  for x in range(count):
    for y in range(count):
      for t in range(4):
        context.set_source_rgb(*color_func(x/count, y/count))
        context.move_to((x + 0.5) * x_step, (y + 0.5) * y_step)
        context.line_to((x + points[t%4 - 1][0]) * x_step, (y + points[t%4 - 1][1]) * y_step)
        context.line_to((x + points[(t + 1)%4 - 1][0]) * x_step, (y + points[(t + 1)%4 - 1][1]) * y_step)
        context.line_to((x + 0.5) * x_step, (y + 0.5) * y_step)
        context.fill_preserve()
        context.stroke()

if __name__ == '__main__':
  arguments = docopt.docopt(__doc__, version='v0.0.0')

  width = int(arguments["--width"])
  height = int(arguments["--height"])

  surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  color_class = FromTopLeftColor() # FromCenterColor()

  if arguments["circle"]:
    draw_circles(surface, color_class, float(arguments["<max-size>"]), int(arguments["<count>"]))
    name = "circles"
  elif arguments["triangle"]:
    draw_triangles(surface, color_class, int(arguments["<count>"]))
    name = "triangles"

  suffix = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
  surface.write_to_png(f"generated/{name}_{suffix}.png")
