"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen

"""
from __future__ import annotations

import datetime
import logging
import cairo
import docopt
import tkinter

from PIL import Image, ImageTk

from color_modes import ColorMode
from color_modes.random2 import Random2ColorMode
from color_modes.sequence2 import Sequence2ColorMode

from models.ui import ColorModeVar

class MainWindow(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height = 1024, 1024
        self.geometry("{}x{}".format(self.width + 50, self.height + 50))

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.image:tkinter.Label = None
        self.common_settings = dict[str, object]()

        self.top_row = self._generate_top_row()

    def _generate_top_row(self):
        top_row = tkinter.Frame(self, name="top_row")
        top_row.grid(column=0, row=0, columnspan=10)

        tkinter.Button(top_row, text="Generate", command=self._draw).grid(row=0, column=0)
        tkinter.Button(top_row, text="Clear", command=self._clear).grid(row=0, column=1)
        tkinter.Button(top_row, text="Save", command=self._save).grid(row=0, column=2)
        tkinter.Button(top_row, text="Reset", command=self._reset).grid(row=0, column=3)

        color_modes = list[ColorMode]([
            Random2ColorMode(top_row),
            Sequence2ColorMode(top_row),
        ])
        self.color_modes = color_modes

        for color_mode in color_modes:
            color_mode.grid(row=2, column=0)
            if color_mode != color_modes[0]:
                color_mode.grid_remove()

        tkinter.Label(top_row, text="Color Mode:").grid(row=1, column=0)
        color_mode_var = ColorModeVar(self, color_modes[0], "color_mode")
        tkinter.OptionMenu(top_row, color_mode_var, *color_modes, command=self._color_mode_changed).grid(row=1, column=1, columnspan=2)
        self.color_mode_var = color_mode_var

        return top_row
    
    def _draw(self):
        if self.image:
            self.image.destroy()

        color_mode = self.color_mode_var.get()
        print(f"Drawing with {color_mode} with type {type(color_mode)}")
        start_time = datetime.datetime.now()

        x_steps = 10
        x_step = self.width/x_steps
        y_steps = 10
        y_step = self.height/y_steps

        for x in range(x_steps):
            for y in range(y_steps):
                self.context.rectangle(x * x_step, y * y_step, x_step, y_step)
                self.context.set_source_rgb(*color_mode.get_color(x/x_steps, y/y_steps).to_tuple())
                self.context.fill()

        time_elapsed = datetime.datetime.now() - start_time

        logging.info(f"Render took {time_elapsed.total_seconds()} seconds")

        self._set_image()

    def _set_image(self):
        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.image = tkinter.Label(self, image=self._image_ref)
        self.image.grid(column=0, row=1, columnspan=10, rowspan=10)

    def _clear_image(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)

    def _clear(self):
        pass

    def _save(self):
        pass

    def _reset(self):
        pass

    def _color_mode_changed(self, *args, **kwargs):
        current_setting = self.color_mode_var.get()

        for color_mode in [x for x in self.color_modes if x != current_setting]:
            color_mode.grid_remove()
        current_setting.grid()

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    logging.basicConfig(level=logging.DEBUG)
    window = MainWindow()
    window.mainloop()

if __name__ == '__main__':
    main()

