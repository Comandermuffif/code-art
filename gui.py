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
from color_modes.gradient import GradientColorMode
from color_modes.modify.normal import NormalColorMode
from color_modes.modify.rotate import RotateColorMode
from color_modes.fire import FireColorMode
from color_modes.grid import GridColorMode
from color_modes.linear_gradient import LinearGradientColorMode

from draw_modes import DrawMode
from draw_modes.circles import CirclesDrawMode
from draw_modes.squares import SquaresDrawMode
from draw_modes.triangles import TrianglesDrawMode
from draw_modes.voronoi import VoronoiDrawMode

from models import FloatColor

from PIL import Image, ImageTk

class DrawUI(tkinter.Tk):
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

        # "ffffff,fff100,ff8c00,e81123,ec008c,68217a,00188f,00bcf2,00b294,009e49,bad80a,000000"
        self.colorMode:ColorMode = NormalColorMode(RotateColorMode(GradientColorMode(FloatColor.getSubcolors(FloatColor.fromHexList("000000,000000,ff8c00,ffffff,00b294,000000,000000"), 7))), 0.03, 0.03)
        self.drawMode:DrawMode = VoronoiDrawMode(250)

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

        start_time = datetime.datetime.now()
        self.drawMode.draw(
            self.context,
            self.colorMode,
            self.width,
            self.height,
        )
        time_elapsed = datetime.datetime.now() - start_time
        logging.info("Draw took %f seconds", time_elapsed.total_seconds())

        start_time = datetime.datetime.now()
        self._setImage()
        time_elapsed = datetime.datetime.now() - start_time
        logging.info("Set took %f seconds", time_elapsed.total_seconds())

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    logging.basicConfig(level=logging.DEBUG)
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
