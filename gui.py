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
import tkinter.colorchooser

from PIL import Image, ImageTk

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

    def add_color(self):
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

        # self.draw()

    def open_options(self):
        self.options_window.deiconify()

    def draw(self):
        if self.image:
            self.image.destroy()

        for c in range(500):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            radious = random.randint(0, 100)

            color = random.choice(self.options_window.color_bar.colors)
            self.context.set_source_rgb(color.r, color.g, color.b)
            self.context.arc(x, y, radious, 0, 360)
            self.context.fill()

        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.image = tkinter.Label(self, image=self._image_ref)
        self.image.grid(column=0, row=1, columnspan=10, rowspan=9)

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
