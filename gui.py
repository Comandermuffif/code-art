"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen

"""
import random
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

class ColorBar(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = list[FloatColor]()
        self.color_labels = list[tkinter.Label]()

        self.add_color_button = tkinter.Button(self, text="Add Color", command=self.add_color)
        self.add_color_button.grid(column=0, row=0)

        self.clear_colors_button = tkinter.Button(self, text="Clear Colors", command=self.clear_colors)
        self.clear_colors_button.grid(column=0, row=1)

        self.add_color(FloatColor(1, 0, 0))
        self.add_color(FloatColor(0, 1, 0))
        self.add_color(FloatColor(0, 0, 1))

    def add_color(self, new_color:FloatColor=None):
        if not new_color:
            chosen_color = tkinter.colorchooser.askcolor()
            new_color = FloatColor(*(x/255 for x in chosen_color[0]))
        self.colors.append(new_color)

        color_label = tkinter.Label(self, background=new_color.to_hex(), width=2, height=1)
        color_label.grid(column=len(self.color_labels) + 1, row=0, rowspan=2)

        self.color_labels.append(color_label)

    def clear_colors(self):
        for label in self.color_labels:
            label.destroy()

        self.colors.clear()
        self.color_labels.clear()

class OptionsWindow(tkinter.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color_bar = ColorBar(self)
        self.color_bar.grid(column=1, row=0, columnspan=9)

        modes = [x[0] for x in inspect.getmembers(DrawModes, lambda a:not(inspect.isroutine(a))) if not(x[0].startswith('__') and x[0].endswith('__'))]
        self.current_mode = tkinter.StringVar(self, modes[0])
        self.mode_selector = tkinter.OptionMenu(self, self.current_mode, *modes)
        self.mode_selector.grid(column=0, row=1)

        self.count_text = tkinter.Text(self, height=1)
        self.count_text.grid(column=1, row=2)

        self.max_text = tkinter.Text(self, height=1)
        self.max_text.grid(column=1, row=3)

        self.obj_count = 500
        self.obj_max_size = 50

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

        self.geometry("{}x{}".format(self.width, self.height))

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.image:tkinter.Label = None

        self.generate_button = tkinter.Button(self, text="Generate", command=self.draw)
        self.generate_button.grid(column=0, row=0)

        self.options_button = tkinter.Button(self, text="Options", command=self.open_options)
        self.options_button.grid(column=1, row=0)

        self.options_window = OptionsWindow(self)
        self.options_window.title("Options")
        self.options_window.geometry("400x400")
        self.options_window.withdraw()

    def open_options(self):
        self.options_window.deiconify()

    def draw(self):
        if self.image:
            self.image.destroy()

        {
            DrawModes.random: self._draw_random,
            DrawModes.bucketed: self._draw_bucketed,
        }[self.options_window.current_mode.get()]()

        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.image = tkinter.Label(self, image=self._image_ref)
        self.image.grid(column=0, row=1, columnspan=10, rowspan=9)

    def _draw_random(self):
        # TODO: Clear the image
        for _ in range(self.options_window.obj_count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            color = RandomColorSelector.get_color(self.options_window.color_bar.colors)
            self.context.set_source_rgb(color.r, color.g, color.b)

            radious = random.randint(0, self.options_window.obj_max_size)
            self.context.arc(x, y, radious, 0, 360)
            self.context.fill()

    def _draw_bucketed(self):
        for _ in range(self.options_window.obj_count):
            x_float = random.random()
            y_float = random.random()

            color = BucketedColor.get_color(x_float, y_float, self.options_window.color_bar.colors)
            self.context.set_source_rgb(color.r, color.g, color.b)

            radious = random.randint(0, self.options_window.obj_max_size)
            self.context.arc(x_float * self.width, y_float * self.height, radious, 0, 360)
            self.context.fill()

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
