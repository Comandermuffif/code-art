"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen
  -v --verbose                Print additional information

"""
from __future__ import annotations
import datetime
import itertools
import logging

import cairo
import docopt
import random
import string
import tkinter

from color_modes import ColorMode
from color_modes.gradient import GradientColorMode
from color_modes.grid import GridColorMode
from color_modes.linear_gradient import LinearGradientColorMode
from color_modes.modify.clamp import ClampColorMode
from color_modes.modify.normal import NormalColorMode
from color_modes.modify.rotate import RotateColorMode

from draw_modes import DrawMode
from draw_modes.circles import CirclesDrawMode
from draw_modes.squares import SquaresDrawMode
from draw_modes.triangles import TrianglesDrawMode
from draw_modes.voronoi import VoronoiDrawMode

from PIL import Image, ImageTk
from models import FloatColor

from models.input import InputParser, Token, FunctionToken, ArrayToken, ValueToken

class Renderer():
    knownFunctions = { x.__name__: x for x in itertools.chain(DrawMode.__subclasses__(), ColorMode.__subclasses__(), [FloatColor.getSubcolors])}

    @classmethod
    def render(cls, tokens:list[Token], context:cairo.Context, width:int, height:int) -> None:
        colorMode:ColorMode = None
        drawMode:DrawMode = None

        for token in tokens:
            if not isinstance(token, FunctionToken):
                raise ValueError("Expected function token at root")

            if token.name == "SetDrawMode":
                if len(token.args) != 1:
                    raise ValueError("Unexpected number of arguments")
                drawMode = cls._flatten(token.args[0])
            elif token.name == "SetColorMode":
                if len(token.args) != 1:
                    raise ValueError("Unexpected number of arguments")
                colorMode = cls._flatten(token.args[0])
            elif token.name == "Draw":
                drawMode.draw(context, colorMode, width, height)
            else:
                raise ValueError(f"Unexpected function name {token.name}")

    @classmethod
    def _flatten(cls, token:Token):
        if isinstance(token, FunctionToken):
            if token.name in cls.knownFunctions:
                return cls.knownFunctions[token.name](*[cls._flatten(x) for x in token.args])

        if isinstance(token, ArrayToken):
            return list([cls._flatten(x) for x in token.items])

        if isinstance(token, ValueToken):
            if token.value.startswith("#"):
                return FloatColor.fromHex(token.value)
            
            if token.value.isdigit():
                return int(token.value)
            return token.value

        raise NotImplementedError()

class DrawUI(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height = 1024, 1024

        self.geometry("{}x{}".format(self.width + 50, self.height + 50))

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.image: tkinter.Label = None

        self._clearImage()

        tkinter.Button(self, text="Generate", command=self.draw).grid(column=0, row=0)
        tkinter.Button(self, text="Clear", command=self._clearImage).grid(column=1, row=0)
        tkinter.Button(self, text="Save", command=self._saveImage).grid(column=2, row=0)

        self.redraw = tkinter.BooleanVar(self, False)
        tkinter.Checkbutton(self, text="Redraw", variable=self.redraw).grid(column=3, row=0)

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

        with open("input.conf", mode='r') as stream:
            tokens = InputParser.parse(stream)

        start_time = datetime.datetime.now()
        Renderer.render(tokens, self.context, self.width, self.height)
        time_elapsed = datetime.datetime.now() - start_time
        logging.info("Draw took %f seconds", time_elapsed.total_seconds())

        start_time = datetime.datetime.now()
        self._setImage()
        time_elapsed = datetime.datetime.now() - start_time
        logging.info("Set took %f seconds", time_elapsed.total_seconds())

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    logging.basicConfig(level=(logging.DEBUG if arguments['--verbose'] else logging.INFO))
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
