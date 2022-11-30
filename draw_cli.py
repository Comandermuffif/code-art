"""Draw

Usage:
  draw_cli.py [options] circle <max-size> <count>
  draw_cli.py [options] triangle <count>

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
  max_distance = 2

  def __init__(self, divergance=0.15):
    self.divergance = divergance

  def get_color(self, x:float, y:float):
    colors = [
      hex_to_rgb("B02E0C"),
      hex_to_rgb("EB4511"),
      hex_to_rgb("E6EFF8"),
      hex_to_rgb("FFFFFF"),
      hex_to_rgb("4E7934"),
      hex_to_rgb("1A4709"),
    ]
    # return self.random_color(colors)
    return self.get_color_bucketed(x, y, colors)

  def random_color(self, colors:list):
    return colors[random.randint(0, len(colors) - 1)]

  def get_color_bucketed(self, x:float, y:float, colors:list=[(1,0,0), (0,1,0), (0,0,1)]):
    buckets = len(colors)
    bucket_width = FromTopLeftColor.max_distance/buckets
    color_prob = []
    for i in range(buckets):
      color_prob.append(None)

    for i in range(buckets):
      color_prob[i] = abs(random.normalvariate(bucket_width * (i + 0.5), self.divergance)  - (x + y))

    max_prob = min(color_prob)
    for i in range(buckets):
      if max_prob == color_prob[i]:
        return colors[i]
    return (0, 0, 0)

  def get_color_gradient(self, x:float, y:float, min_hue:float=0.16, max_hue:float=0.3):
    distance_from_corner = x + y
    hue = distance_from_corner/FromTopLeftColor.max_distance
    hue = min(1, max(0, hue + (random.random() - 0.5) * self.divergance))
    hue = ((max_hue - min_hue) * hue) + min_hue
    return colorsys.hsv_to_rgb(hue, 1, 1)

def hex_to_rgb(hex:str):
  hex = int(hex, 16)
  return (
    ((hex >> 16) & 0xFF)/255,
    ((hex >> 8) & 0xFF)/255,
    ((hex >> 0) & 0xFF)/255,
  )

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
