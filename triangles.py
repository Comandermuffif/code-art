"""Triangles

Usage:
  triangles.py options

Options:
  -h --help                   Show this screen
  -W --width <px>             The width of the image to create in pixels [default: 2048]
  -H --height <px>            The height of the image to create in pixels [default: 2048]
  -t --triangles <triangles>  The number of triangle squares on one edge [default: 50]

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

def get_color_greyscale():
  return lambda x, y: colorsys.hsv_to_rgb(0, 0, random.random())

def get_color_rainbow(divergance=0.1):
  return lambda x, y: colorsys.hsv_to_rgb(x + random.random()*divergance, 1, 1)

def get_color_binary_func(left_color, right_color):
  return lambda x, y: left_color if x > random.gauss(0.5, .2) else right_color

def get_color_circle(circle_color, other_color):
  return lambda x, y: other_color if math.sqrt(math.pow(x-0.5, 2) + math.pow(y-0.5, 2)) > random.gauss(0.35, .1) else circle_color

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='Triangles')

    width = int(arguments["--width"])
    height = int(arguments["--height"])
    triangles = int(arguments["--triangles"])

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_line_width(1)

    x_step = width/triangles
    y_step = height/triangles

    color_func = get_color_binary_func(
      (random.random(), random.random(), random.random()),
      (random.random(), random.random(), random.random())
    )

    if arguments["--rainbow"]:
      color_func = get_color_rainbow()
    if arguments["--greyscale"] or True:
      color_func = get_color_greyscale()
    if arguments["--circle"]:
      color_func = get_color_circle(
        (random.random(), random.random(), random.random()),
        (random.random(), random.random(), random.random())
      )

    points = [
      (0, 0),
      (0, 1),
      (1, 1),
      (1, 0)
    ]

    for x in range(triangles):
      for y in range(triangles):
        for t in range(4):
          ctx.set_source_rgb(*color_func(x/triangles, y/triangles))
          ctx.move_to((x + 0.5) * x_step, (y + 0.5) * y_step)
          ctx.line_to((x + points[t%4 - 1][0]) * x_step, (y + points[t%4 - 1][1]) * y_step)
          ctx.line_to((x + points[(t + 1)%4 - 1][0]) * x_step, (y + points[(t + 1)%4 - 1][1]) * y_step)
          ctx.line_to((x + 0.5) * x_step, (y + 0.5) * y_step)
          ctx.fill_preserve()
          ctx.stroke()
    
    name = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
    surface.write_to_png(f"generated/{name}.png")