"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen

"""
from __future__ import annotations

import random
import string
import cairo
import docopt
import tkinter
import tkinter.colorchooser
import inspect

from abc import abstractclassmethod

from PIL import Image, ImageTk

class DrawModes():
    random = "random"
    bucketed = "bucketed"

class FloatColor():
    def __init__(self, r:float, g:float, b:float):
        self.r = r
        self.g = g
        self.b = b

    def to_hex(self):
        hex(int(self.g * 255))
        return "#{:02x}{:02x}{:02x}".format(int(self.r * 255), int(self.g * 255), int(self.b * 255)).upper()

    @classmethod
    def from_hex(cls, input:str) -> FloatColor:
        input = input.strip().strip('#')
        parts = tuple(int(input[i:i+2], 16) for i in (0, 2, 4))
        return FloatColor(parts[0]/255, parts[1]/255, parts[2]/255)

class OptionsFrame(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Row 0
        tkinter.Label(self, text="Colors:").grid(column=0, row=0)
        self._color_entry = tkinter.Entry(self)
        self._color_entry.grid(column=1, row=0)
        self._color_entry.insert(tkinter.END, "FF0000, 00FF00, 0000FF")

        # Row 1
        tkinter.Label(self, text="Mode:").grid(column=0, row=1)
        modes = [x[0] for x in inspect.getmembers(DrawModes, lambda a:not(inspect.isroutine(a))) if not(x[0].startswith('__') and x[0].endswith('__'))]
        self.current_mode = tkinter.StringVar(self, modes[0])
        self._mode_selector = tkinter.OptionMenu(self, self.current_mode, *modes)
        self._mode_selector.grid(column=1, row=1)

        # Row 2
        tkinter.Label(self, text="Count:").grid(column=0, row=2)
        self._count_entry = tkinter.Entry(self)
        self._count_entry.grid(column=1, row=2)
        self._count_entry.insert(tkinter.END, "500")

        # Row 3
        tkinter.Label(self, text="Max Size:").grid(column=0, row=3)
        self._max_entry = tkinter.Entry(self)
        self._max_entry.grid(column=1, row=3)
        self._max_entry.insert(tkinter.END, "50")

    def get_mode(self) -> str:
        return self.current_mode.get()

    def get_count(self) -> int:
        return int(self._count_entry.get())

    def get_max_size(self) -> int:
        return int(self._max_entry.get())

    def get_colors(self) -> list[FloatColor]:
        return [
            FloatColor.from_hex(x) for x in self._color_entry.get().split(',')
        ]

class ColorSelector(object):
    @abstractclassmethod
    def get_color(x:float, y:float, colors:list[FloatColor]):
        pass

    @abstractclassmethod
    def get_color(colors:list[FloatColor]):
        pass

class RandomColorSelector(ColorSelector):
    @classmethod
    def get_color(cls, colors:list[FloatColor]):
        return random.choice(colors)

class BucketedColor(ColorSelector):
    max_distance = 2

    @classmethod
    def get_color(cls, x:float, y:float, colors:list[FloatColor], divergance:float=0.15):
        buckets = len(colors)
        bucket_width = cls.max_distance/buckets
        color_prob = []

        for i in range(buckets):
            color_prob.append(None)

        for i in range(buckets):
            color_prob[i] = abs(random.normalvariate(bucket_width * (i + 0.5), divergance)  - (x + y))

        max_prob = min(color_prob)
        for i in range(buckets):
            if max_prob == color_prob[i]:
                return colors[i]
        return (0, 0, 0)


class DrawUI(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height = 1024, 1024

        self.geometry("{}x{}".format(self.width + 50, self.height + 50))

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.image:tkinter.Label = None

        self._clear_image()

        self.generate_button = tkinter.Button(self, text="Generate", command=self.draw)
        self.generate_button.grid(column=0, row=0)

        self.options_button = tkinter.Button(self, text="Options", command=self.toggle_options)
        self.options_button.grid(column=1, row=0)

        tkinter.Button(self, text="Clear", command=self._clear_image).grid(column=2, row=0)
        tkinter.Button(self, text="Save", command=self._save_image).grid(column=3, row=0)

        self._options = OptionsFrame(self)
        self._options.grid(column=0, row=1, columnspan=10)
        self._options.grid_remove()

    def toggle_options(self):
        if len(self._options.grid_info()) == 0:
            self._options.grid()
        else:
            self._options.grid_remove()

    def _clear_image(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)

        self._set_image()

    def _set_image(self):
        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.image = tkinter.Label(self, image=self._image_ref)
        self.image.grid(column=0, row=2, columnspan=10, rowspan=9)

    def draw(self):
        if self.image:
            self.image.destroy()

        {
            DrawModes.random: self._draw_random,
            DrawModes.bucketed: self._draw_bucketed,
        }[self._options.get_mode()]()

        self._set_image()

    def _draw_random(self):
        for _ in range(self._options.get_count()):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            color = RandomColorSelector.get_color(self._options.get_colors())
            self.context.set_source_rgb(color.r, color.g, color.b)

            radious = random.randint(0, self._options.get_max_size())
            self.context.arc(x, y, radious, 0, 360)
            self.context.fill()

    def _draw_bucketed(self):
        for _ in range(self._options.get_count()):
            x_float = random.random()
            y_float = random.random()

            color = BucketedColor.get_color(x_float, y_float, self._options.get_colors())
            self.context.set_source_rgb(color.r, color.g, color.b)

            radious = random.randint(0, self._options.get_max_size())
            self.context.arc(x_float * self.width, y_float * self.height, radious, 0, 360)
            self.context.fill()

    def _save_image(self):
        name = self._options.get_mode()
        suffix = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
        self.surface.write_to_png(f"generated/{name}_{suffix}.png")

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
