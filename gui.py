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

from color_modes import ColorMode
from color_modes.invert import InvertColorMode
from color_modes.random import RandomColorMode
from color_modes.gradient import GradientColorMode

from draw_modes import DrawMode
from draw_modes.circles import CirclesDrawMode
from draw_modes.lines import LinesDrawMode
from draw_modes.overlapping_circles import OverlappingCirclesDrawMode
from draw_modes.splines import SpinesDrawMode
from draw_modes.squares import SquaresDrawMode
from draw_modes.text import TextDrawMode
from draw_modes.triangles import TrianglesDrawMode

from models import FloatColor

from PIL import Image, ImageTk

class OptionsFrame(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Row 0
        tkinter.Label(self, text="Colors:").grid(column=0, row=0)
        self._color_entry = tkinter.Entry(self)
        self._color_entry.grid(column=1, row=0)
        self._color_entry.insert(tkinter.END, "fff100,ff8c00,e81123,ec008c,68217a,00188f,00bcf2,00b294,009e49,bad80a")

        # Row 1
        tkinter.Label(self, text="Color Mode:").grid(column=0, row=1)
        self.color_modes = {
            x.get_name(): x for x in list[type[ColorMode]]([
                GradientColorMode,
                InvertColorMode,
                RandomColorMode,
            ])
        }
        color_mode_keys = list(self.color_modes.keys())
        self.current_color_mode_key = tkinter.StringVar(self, color_mode_keys[0])
        self.current_color_mode_key.trace_add("write", self._color_mode_changed)
        self.color_mode_selector = tkinter.OptionMenu(self, self.current_color_mode_key, *color_mode_keys)
        self.color_mode_selector.grid(column=1, row=1)

        # Row 2
        tkinter.Label(self, text="Color Options:").grid(column=0, row=2, columnspan=2)

        # Row 3
        self.color_mode_options_frame = tkinter.Frame(self)
        self.color_mode_options_frame.grid(column=0, row=3, columnspan=2)
        self.color_mode_settings_entry = {}

        # Row 4
        tkinter.Label(self, text="Draw Mode:").grid(column=0, row=4)
        self.draw_modes = {
            x.get_name(): x for x in list[type[DrawMode]]([
                TrianglesDrawMode,
                CirclesDrawMode,
                SquaresDrawMode,
                LinesDrawMode,
                SpinesDrawMode,
                TextDrawMode,
                OverlappingCirclesDrawMode,
            ])
        }
        draw_mode_keys = list(self.draw_modes.keys())
        self.current_draw_mode_key = tkinter.StringVar(self, draw_mode_keys[0])
        self.current_draw_mode_key.trace_add("write", self._draw_mode_changed)
        self.draw_mode_selector = tkinter.OptionMenu(self, self.current_draw_mode_key, *draw_mode_keys)
        self.draw_mode_selector.grid(column=1, row=4)

        # Row 5
        tkinter.Label(self, text="Draw Options:").grid(column=0, row=5, columnspan=2)

        # Row 6
        self.draw_mode_options_frame = tkinter.Frame(self)
        self.draw_mode_options_frame.grid(column=0, row=6, columnspan=2)
        self.draw_mode_settings_entry = {}

        # Finalize
        self._color_mode_changed()
        self._draw_mode_changed()

    def get_colors(self) -> list[FloatColor]:
        return [
            FloatColor.from_hex(x) for x in self._color_entry.get().split(',')
        ]

    def get_color_mode(self) -> str:
        return self.current_color_mode_key.get()

    def get_draw_mode(self) -> str:
        return self.current_draw_mode_key.get()

    def _color_mode_changed(self, *args, **kwargs) -> None:
        children = list(self.color_mode_options_frame.children.values())
        for child in children:
            child.destroy()

        mode = self.color_modes[self.get_color_mode()]
        self.color_mode_settings_entry = {}

        count = 0
        for (key, (name, type, default_value)) in mode.get_option_types().items():
            label = tkinter.Label(self.color_mode_options_frame, text=name)
            label.grid(row=count, column=0)
            entry = tkinter.Entry(self.color_mode_options_frame)
            entry.grid(row=count, column=1)
            entry.insert(tkinter.END, default_value)

            self.color_mode_settings_entry[key] = entry
            count = count + 1

    def _draw_mode_changed(self, *args, **kwargs) -> None:
        children = list(self.draw_mode_options_frame.children.values())
        for child in children:
            child.destroy()

        mode = self.draw_modes[self.get_draw_mode()]
        self.draw_mode_settings_entry = {}

        count = 0
        for (key, (name, type, default_value)) in mode.get_option_types().items():
            label = tkinter.Label(self.draw_mode_options_frame, text=name)
            label.grid(row=count, column=0)
            entry = tkinter.Entry(self.draw_mode_options_frame)
            entry.grid(row=count, column=1)
            entry.insert(tkinter.END, default_value)

            self.draw_mode_settings_entry[key] = entry
            count = count + 1

    def get_color_mode_settings(self):
        return {
            key: entry.get()
            for (key, entry) in
            self.color_mode_settings_entry.items()
        }

    def get_draw_mode_settings(self):
        return {
            key: entry.get()
            for (key, entry) in
            self.draw_mode_settings_entry.items()
        }

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

        # Reset the operator, it case something changed it (invert....)
        self.context.set_operator(cairo.Operator.OVER)

        color_mode_key = self._options.get_color_mode()
        color_mode_class = self._options.color_modes[color_mode_key]

        color_mode = color_mode_class(self._options.get_colors(), **self._options.get_color_mode_settings(), context=self.context)

        draw_mode_key = self._options.get_draw_mode()
        draw_mode_class = self._options.draw_modes[draw_mode_key]

        draw_mode = draw_mode_class(**self._options.get_draw_mode_settings())

        draw_mode.draw(
            self.context,
            color_mode,
            self.width,
            self.height,
        )

        self._set_image()

    def _save_image(self):
        color_mode = self._options.get_color_mode()
        draw_mode = self._options.get_draw_mode()
        suffix = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
        self.surface.write_to_png(f"generated/{color_mode}_{draw_mode}_{suffix}.png")

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
