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
from color_modes.cluster import ClusterColorMode
from color_modes.invert import InvertColorMode
from color_modes.random import RandomColorMode
from color_modes.gradient import GradientColorMode
from color_modes.sequence import SequenceColorMode

from draw_modes import DrawMode
from draw_modes.circles import CirclesDrawMode
from draw_modes.cluster2 import Cluster2DrawMode
from draw_modes.cluster3 import Cluster3DrawMode
from draw_modes.lines import LinesDrawMode
from draw_modes.overlapping_circles import OverlappingCirclesDrawMode
from draw_modes.splines import SpinesDrawMode
from draw_modes.squares import SquaresDrawMode
from draw_modes.text import TextDrawMode
from draw_modes.triangles import TrianglesDrawMode

from models import FloatColor

from PIL import Image, ImageTk

class ColorModeSettingsFrame(tkinter.Frame):
    def __init__(self, color_mode:ColorMode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_mode = color_mode
        self.settings_variables = dict[str, tkinter.Variable]()

        count = 0
        for (option_key, (name, type, default_value)) in self.color_mode.get_option_types().items():
            label = tkinter.Label(self, text=name)
            label.grid(row=count, column=0)

            if type == bool:
                variable = tkinter.BooleanVar(value=default_value)
                entry = tkinter.Checkbutton(self, onvalue=True, offvalue=False, variable=variable)
            elif type == float:
                variable = tkinter.DoubleVar(value=default_value)
                entry = tkinter.Entry(self, textvariable=variable)
            elif type == int:
                variable = tkinter.IntVar(value=default_value)
                entry = tkinter.Entry(self, textvariable=variable)
            else:
                variable = tkinter.StringVar(value=default_value)
                entry = tkinter.Entry(self, textvariable=variable)

            self.settings_variables[option_key] = variable
            entry.grid(row=count, column=1)
            count += 1

        if count == 0:
            tkinter.Label(self, text="N/A").grid(row=0, column=0)

    def get_settings(self):
        return {
            key: entry.get()
            for (key, entry) in
            self.settings_variables.items()
        }

class DrawModeSettingsFrame(tkinter.Frame):
    def __init__(self, draw_mode:DrawMode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.draw_mode = draw_mode
        self.settings_variables = dict[str, tkinter.Variable]()

        count = 0
        for (option_key, (name, type, default_value)) in self.draw_mode.get_option_types().items():
            label = tkinter.Label(self, text=name)
            label.grid(row=count, column=0)

            if type == bool:
                variable = tkinter.BooleanVar(value=default_value)
                entry = tkinter.Checkbutton(self, onvalue=True, offvalue=False, variable=variable)
            elif type == float:
                variable = tkinter.DoubleVar(value=default_value)
                entry = tkinter.Entry(self, textvariable=variable)
            elif type == int:
                variable = tkinter.IntVar(value=default_value)
                entry = tkinter.Entry(self, textvariable=variable)
            else:
                variable = tkinter.StringVar(value=default_value)
                entry = tkinter.Entry(self, textvariable=variable)

            self.settings_variables[option_key] = variable
            entry.grid(row=count, column=1)
            count += 1

        if count == 0:
            tkinter.Label(self, text="N/A").grid(row=0, column=0)

    def get_settings(self):
        return {
            key: entry.get()
            for (key, entry) in
            self.settings_variables.items()
        }

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
                ClusterColorMode,
                InvertColorMode,
                RandomColorMode,
                SequenceColorMode,
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
        self.color_mode_settings = tkinter.Frame(self)
        self.color_mode_settings.grid(column=0, row=3, columnspan=2)
        self.color_mode_settings_frames = dict[str, ColorModeSettingsFrame]()

        # Row 4
        tkinter.Label(self, text="Draw Mode:").grid(column=0, row=4)
        self.draw_modes = {
            x.get_name(): x for x in list[type[DrawMode]]([
                Cluster3DrawMode,
                Cluster2DrawMode,
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
        self.draw_mode_settings = tkinter.Frame(self)
        self.draw_mode_settings.grid(column=0, row=6, columnspan=2)
        self.draw_mode_settings_frames = dict[str, DrawModeSettingsFrame]()

        # Finalize
        self._set_color_mode_settings()
        self._set_draw_mode_settings()
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

    def _set_color_mode_settings(self):
        # For every color mode
        for (color_mode_key, color_mode) in self.color_modes.items():
            color_mode_settings_frame = ColorModeSettingsFrame(color_mode, self.color_mode_settings)
            self.color_mode_settings_frames[color_mode_key] = color_mode_settings_frame

            color_mode_settings_frame.grid(row=1, column=1)
            color_mode_settings_frame.grid_remove()

    def _set_draw_mode_settings(self):
        # For every color mode
        for (draw_mode_key, draw_mode) in self.draw_modes.items():
            draw_mode_settings_frame = DrawModeSettingsFrame(draw_mode, self.draw_mode_settings)
            self.draw_mode_settings_frames[draw_mode_key] = draw_mode_settings_frame

            draw_mode_settings_frame.grid(row=1, column=1)
            draw_mode_settings_frame.grid_remove()

    def _color_mode_changed(self, *args, **kwargs) -> None:
        # Hide all frames
        for (color_mode_key, color_mode_settings_frame) in self.color_mode_settings_frames.items():
            color_mode_settings_frame.grid_remove()

        self.color_mode_settings_frames[self.get_color_mode()].grid()

    def _draw_mode_changed(self, *args, **kwargs) -> None:
        # Hide all frames
        for (draw_mode_key, draw_mode_settings_frame) in self.draw_mode_settings_frames.items():
            draw_mode_settings_frame.grid_remove()

        self.draw_mode_settings_frames[self.get_draw_mode()].grid()

    def get_color_mode_settings(self):
        return self.color_mode_settings_frames[self.get_color_mode()].get_settings()

    def get_draw_mode_settings(self):
        return self.draw_mode_settings_frames[self.get_draw_mode()].get_settings()

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
