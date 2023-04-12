"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen

"""
from __future__ import annotations
import datetime
import logging

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
from draw_modes.lines import LinesDrawMode
from draw_modes.overlapping_circles import OverlappingCirclesDrawMode
from draw_modes.splines import SpinesDrawMode
from draw_modes.squares import SquaresDrawMode
from draw_modes.text import TextDrawMode
from draw_modes.triangles import TrianglesDrawMode
from draw_modes.voronoi import VoronoiDrawMode

from models import FloatColor
from models.input import ValueToken, parse, ArrayToken, FuncToken

from PIL import Image, ImageTk

class DrawUI(tkinter.Tk):
    knownDrawModes = dict[str, type[DrawMode]]({
        "Voronoi": VoronoiDrawMode,
        "Circles": CirclesDrawMode
    })

    knownColorModes = dict[str, type[ColorMode]]({
        "Gradient": GradientColorMode
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height = 1024, 1024

        self.geometry("{}x{}".format(self.width + 50, self.height + 50))

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.image:tkinter.Label = None

        self._clearImage()

        tkinter.Button(self, text="Generate", command=self.draw).grid(column=0, row=0)
        tkinter.Button(self, text="Clear", command=self._clearImage).grid(column=1, row=0)
        tkinter.Button(self, text="Save", command=self._saveImage).grid(column=2, row=0)

        self.command = tkinter.Text(self, height=1)
        self.command.insert(1.0, "Voronoi(Gradient([fff100,ff8c00,e81123,ec008c,68217a,00188f,00bcf2,00b294,009e49,bad80a]))")
        self.command.grid(row=1, column=0, columnspan=3)

    def _clearImage(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self._setImage()

    def _setImage(self):
        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.image = tkinter.Label(self, image=self._image_ref)
        self.image.grid(column=0, row=2, columnspan=10, rowspan=9)

    def _saveImage(self):
        color_mode = ""
        draw_mode = ""
        suffix = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
        self.surface.write_to_png(f"generated/{color_mode}_{draw_mode}_{suffix}.png")

    def draw(self):
        if self.image:
            self.image.destroy()

        # Reset the operator, it case something changed it (invert....)
        self.context.set_operator(cairo.Operator.OVER)

        command = parse(self.command.get(1.0, 'end'))
        if (not isinstance(command, FuncToken)):
            return
        drawMode = self.knownDrawModes[command.name](count=3000)

        if (len(command.args) < 1):
            return
        
        colorModeToken = command.args[0]
        if (not isinstance(colorModeToken, FuncToken)):
            return
        
        colorsArray = colorModeToken.args[0]
        if (not isinstance(colorsArray, ArrayToken)):
            return
        colors = [FloatColor.from_hex(x.value) for x in colorsArray.values if isinstance(x, ValueToken)]
        colorMode = self.knownColorModes[colorModeToken.name](colors, angle=45, divergance=0.1)

        start_time = datetime.datetime.now()

        drawMode.draw(
            self.context,
            colorMode,
            self.width,
            self.height,
        )

        time_elapsed = datetime.datetime.now() - start_time

        logging.info(f"Render took {time_elapsed.total_seconds()} seconds")

        self._setImage()

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    logging.basicConfig(level=logging.DEBUG)
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
