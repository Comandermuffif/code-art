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
from draw_modes.bucketed import BucketedDrawMode
from draw_modes.gradient import GradientDrawMode
from draw_modes.random import RandomDrawMode

from models import FloatColor

from PIL import Image, ImageTk

class OptionsFrame(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Row 0
        tkinter.Label(self, text="Colors:").grid(column=0, row=0)
        self._color_entry = tkinter.Entry(self)
        self._color_entry.grid(column=1, row=0)
        # ff0000,ffa500,ffff00,008000,0000ff,4b0082,ee82ee
        self._color_entry.insert(tkinter.END, "FF0000, 00FF00, 0000FF")

        # Row 1
        tkinter.Label(self, text="Color Mode:").grid(column=0, row=1)
        self.modes = {
            x.get_name(): x for x in [
                GradientDrawMode(),
                BucketedDrawMode(),
                RandomDrawMode(),
            ]
        }

        mode_keys = list(self.modes.keys())

        self.current_mode_key = tkinter.StringVar(self, mode_keys[0])
        self.current_mode_key.trace("w", self._mode_changed)

        self._mode_selector = tkinter.OptionMenu(self, self.current_mode_key, *mode_keys)
        self._mode_selector.grid(column=1, row=1)

        tkinter.Label(self, text="Mode Options:").grid(column=0, row=2, columnspan=2)
        self._mode_options_frame = tkinter.Frame(self)
        self._mode_options_frame.grid(column=0, row=3, columnspan=2)
        self._mode_settings_entry = {}

        self._mode_changed()

    def get_mode(self) -> str:
        return self.current_mode_key.get()

    def get_colors(self) -> list[FloatColor]:
        return [
            FloatColor.from_hex(x) for x in self._color_entry.get().split(',')
        ]

    def get_mode_settings(self):
        return {
            key: entry.get()
            for (key, entry) in
            self._mode_settings_entry.items()
        }

    def _mode_changed(self, *args, **kwargs):
        for child in self._mode_options_frame.children.values():
            child.destroy()

        mode = self.modes[self.get_mode()]
        self._mode_settings_entry = {}

        count = 0

        for (key, (name, type, default_value)) in mode.get_option_types().items():
            label = tkinter.Label(self._mode_options_frame, text=name)
            label.grid(row=count, column=0)
            entry = tkinter.Entry(self._mode_options_frame)
            entry.grid(row=count, column=1)
            entry.insert(tkinter.END, default_value)

            self._mode_settings_entry[key] = entry

            count = count + 1

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

        mode_key = self._options.get_mode()
        mode = self._options.modes[mode_key]
        mode.draw(
            self.context,
            self._options.get_colors(),
            width=self.width,
            height=self.height,
            **self._options.get_mode_settings(),
        )

        self._set_image()

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
