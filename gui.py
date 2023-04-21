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
import yaml
import json
import jsonschema

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

class InputParser(object):
    knownDrawMode = {
        'circles': CirclesDrawMode,
        'squares': SquaresDrawMode,
        'triangles': TrianglesDrawMode,
        'voronoi': VoronoiDrawMode,
    }

    knownColorModes = {
        'gradient': GradientColorMode,
        'normal': NormalColorMode,
        'rotate': RotateColorMode,
        'linearGradient': LinearGradientColorMode
    }

    with open('input.schema.json') as stream:
        inputSchema = json.load(stream)

    @classmethod
    def parse(cls, filename:str) -> tuple[ColorMode, DrawMode]:
        colorMode:ColorMode = None
        drawMode:DrawMode = None

        with open(filename, 'r') as stream:
            data = yaml.safe_load(stream)

        try:
            jsonschema.validate(data, cls.inputSchema)
        except jsonschema.ValidationError as error:
            logging.exception("Failed to validate %s", filename, exc_info=error)
            return (colorMode, drawMode)

        if not isinstance(data, dict) or 'drawMode' not in data or 'colorMode' not in data:
            return (colorMode, drawMode)

        drawData = data["drawMode"]
        colorData = data["colorMode"]

        if not isinstance(drawData, dict) or not isinstance(colorData, dict):
            return (colorMode, drawMode)
        
        drawMode = cls._parseValue(drawData)
        colorMode = cls._parseValue(colorData)

        return (colorMode, drawMode)

    @classmethod
    def _parseValue(cls, value) -> object:
        if isinstance(value, str):
            if value.startswith('#'):
                parsedColor = FloatColor.fromHex(value)
                if parsedColor != None:
                    return parsedColor
        if isinstance(value, list):
            return [cls._parseValue(x) for x in value]
        if isinstance(value, dict):
            if len(value) == 1:
                (key, subValue) = next(iter(value.items()))
                if key in cls.knownColorModes:
                    return cls.knownColorModes[key](**cls._parseValue(subValue))
                elif key in cls.knownDrawMode:
                    return cls.knownDrawMode[key](**cls._parseValue(subValue))
                elif key == "getSubcolors":
                    return FloatColor.getSubcolors(**cls._parseValue(subValue))
            return {
                k: cls._parseValue(v) for k,v in value.items()
            }
        return value

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
        (colorMode, drawMode) = InputParser.parse("input.yml")

        if colorMode == None or drawMode == None:
            return

        if self.image:
            self.image.destroy()

        start_time = datetime.datetime.now()
        drawMode.draw(
            self.context,
            colorMode,
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
