"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen

"""
import math
import random
import cairo
import docopt
import tkinter

from PIL import Image, ImageTk

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    window = tkinter.Tk()

    width, height = 1024, 1024
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)

    min_hue = tkinter.Scale(window, from_=0, to=100, orient=tkinter.HORIZONTAL, length=width/2)
    max_hue = tkinter.Scale(window, from_=0, to=100, orient=tkinter.HORIZONTAL, length=width/2)
    image_label = tkinter.Label(window, text="1")

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    context.set_source_rgb(random.random(), random.random(), random.random())
    context.arc(512, 512, 50, 0, 360)
    context.fill()
    data = Image.frombuffer("RGBA", (width, height), surface.get_data().tobytes(), "raw", "BGRA", 0, 1)
    generated_image_a = ImageTk.PhotoImage(data)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    context.set_source_rgb(random.random(), random.random(), random.random())
    context.arc(512, 512, 50, 0, 360)
    context.fill()
    data = Image.frombuffer("RGBA", (width, height), surface.get_data().tobytes(), "raw", "BGRA", 0, 1)
    generated_image_b = ImageTk.PhotoImage(data)

    settings = {
      "a_side": True,
      "a_image": generated_image_a,
      "b_image": generated_image_b,
    }

    def gen_callback():
        print("Button start")
        settings["a_side"] = not settings["a_side"]
        if settings["a_side"]:
          image_label.config(image=generated_image_a)
        else:
          image_label.config(image=generated_image_b)
        print("Button end")

    gen_button = tkinter.Button(window, text="Generate", command=gen_callback)

    settings["a_side"] = not settings["a_side"]
    if settings["a_side"]:
      image_label.config(image=generated_image_a)
    else:
      image_label.config(image=generated_image_b)

    min_hue.pack()
    max_hue.pack()
    gen_button.pack()
    image_label.pack(expand=True, fill="both")

    window.mainloop()
