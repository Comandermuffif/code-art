"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen

"""
import math
import docopt
import tkinter
import cairo
from PIL import Image, ImageTk
import colorsys
import random

def random_color():
    return colorsys.hsv_to_rgb(random.random(), 1, 1)

def get_linear_color(x, y):
    if x > 1 or x < 0:
        raise Exception()
    if y > 1 or y < 0:
        raise Exception()

    hue = math.sqrt(math.pow(x - 0.5, 2) + math.pow(y - 0.5, 2)) / math.sqrt(.5)
    return colorsys.hsv_to_rgb(hue, 1, 1)

def get_color(x, y, x_center=0, y_center=0, divergance=0.35):
    distance_from_corner = (x - x_center) + (y - y_center)
    hue = distance_from_corner/math.sqrt(2) + (random.random() - 0.5) * divergance
    # hue = min(1, max(0, hue))
    return colorsys.hsv_to_rgb(hue, 1, 1)

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    window = tkinter.Tk()

    width, height = 1024, 1024
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    max_size = 50
    total_x = int(width/max_size) + 1
    total_y = int(height/max_size) + 1

    x_list = list(range(total_x))
    y_list = list(range(total_y))
    random.shuffle(x_list)
    for xx in x_list:
        random.shuffle(y_list)
        for yy in y_list:
            x = (xx + 0.5 + (random.random() - 0.5) * 1.0) * max_size
            y = (yy + 0.5 + (random.random() - 0.5) * 1.0) * max_size

            context.set_source_rgb(*get_linear_color(xx/total_x, yy/total_y))
            context.arc(x, y, max_size, 0, 360)
            context.fill()

    # count = 3000
    # for _ in range(count):
    #     x = random.random()
    #     y = random.random()
    #     size = random.random() * max_size
    #     context.set_source_rgb(*get_color(x, y))
    #     context.arc(x * width, y * height, size, 0, 360)
    #     context.fill()

    data = Image.frombuffer("RGBA", (width, height), surface.get_data().tobytes(), "raw", "BGRA", 0, 1)
    generated_image = ImageTk.PhotoImage(data)
    tkinter.Label(window, image=generated_image).pack(expand=True, fill="both")

    window.mainloop()
