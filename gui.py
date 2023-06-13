"""Draw

Usage:
  draw_ui.py [options]
  draw_ui.py generate [options]

Options:
  -h --help                   Show this screen

"""
from __future__ import annotations
import datetime
import inspect
import logging
import os

import cairo
import docopt
import json
import jsonschema
import random
import string
import tkinter
import typing
import yaml

from color_modes import ColorMode
from color_modes.gradient import GradientColorMode
from color_modes.grid import GridColorMode
from color_modes.linear_gradient import LinearGradientColorMode
from color_modes.modify.clamp import ClampColorMode
from color_modes.modify.normal import NormalColorMode
from color_modes.modify.transform import TransformColorMode

from draw_modes import DrawMode
from draw_modes.circles import CirclesDrawMode
from draw_modes.squares import SquaresDrawMode
from draw_modes.triangles import TrianglesDrawMode
from draw_modes.voronoi import VoronoiDrawMode

from models import FloatColor

from PIL import Image, ImageTk


class InputParser(object):
    knownDrawMode = { x.__name__: x for x in DrawMode.__subclasses__() }
    knownColorModes = { x.__name__: x for x in ColorMode.__subclasses__() }

    try:
        with open('input.schema.json') as stream:
            inputSchema = json.load(stream)
    except:
        inputSchema = None

    @classmethod
    def parse(cls, filename: str) -> typing.Generator[tuple[ColorMode, DrawMode]]:
        with open(filename, 'r') as stream:
            for data in yaml.safe_load_all(stream):
                try:
                    jsonschema.validate(data, cls.inputSchema)
                except jsonschema.ValidationError as error:
                    logging.exception("Failed to validate %s",
                                      filename, exc_info=error)
                    continue

                if not isinstance(data, dict) or 'drawMode' not in data or 'colorMode' not in data:
                    continue

                drawData = data["drawMode"]
                colorData = data["colorMode"]

                if not isinstance(drawData, dict) or not isinstance(colorData, dict):
                    continue

                yield (cls._parseValue(colorData), cls._parseValue(drawData))

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
                k: cls._parseValue(v) for k, v in value.items()
            }
        return value


class DrawUI(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height = 1024, 1024

        self.geometry("{}x{}".format(self.width + 50, self.height + 50))

        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.image: tkinter.Label = None

        self._clearImage()

        tkinter.Button(self, text="Generate",
                       command=self.draw).grid(column=0, row=0)
        tkinter.Button(self, text="Clear", command=self._clearImage).grid(
            column=1, row=0)
        tkinter.Button(self, text="Save", command=self._saveImage).grid(
            column=2, row=0)

        self.redraw = tkinter.BooleanVar(self, False)
        tkinter.Checkbutton(self, text="Redraw",
                            variable=self.redraw).grid(column=3, row=0)

        self.inputModifiedTime: float = None
        self.colorModes: list[tuple[ColorMode, DrawMode]] = []

        self.after(700, self._checkInput)

    def _checkInput(self, inputFile="input.yml") -> None:
        newModifiedTime = os.path.getmtime(inputFile)
        fileChanged = self.inputModifiedTime == None or newModifiedTime > self.inputModifiedTime
        if fileChanged:
            self.inputModifiedTime = newModifiedTime
            self.colorModes = list(InputParser.parse(inputFile))

        existingDelay = 700
        startTime = datetime.datetime.now()
        if fileChanged or self.redraw.get():
            self.draw()
        existingDelay = existingDelay - \
            int((datetime.datetime.now() - startTime).total_seconds() * 1000)
        self.after(existingDelay, self._checkInput)

    def _clearImage(self):
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self._setImage()

    def _setImage(self):
        self._image_ref = ImageTk.PhotoImage(Image.frombuffer(
            "RGBA", (self.width, self.height), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.image = tkinter.Label(self, image=self._image_ref)
        self.image.grid(column=0, row=2, columnspan=10, rowspan=9)

    def _saveImage(self):
        color_mode = ""
        draw_mode = ""
        suffix = ''.join(random.choice(
            string.ascii_lowercase+string.digits) for _ in range(8))
        self.surface.write_to_png(
            f"generated/{color_mode}_{draw_mode}_{suffix}.png")

    def draw(self):

        if self.image:
            self.image.destroy()

        for (colorMode, drawMode) in self.colorModes:
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


class SchemaGenerator():
    @classmethod
    def generate(cls):
        with open('input.schema.json', 'w') as stream:
            schema = {
                "$id": "https://example.com/input.schema.json",
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Input",
                "type": "object",
                "properties": {
                    "drawMode": DrawMode,
                    "colorMode": ColorMode
                },
                "required": [
                    "drawMode",
                    "colorMode"
                ],
                "$defs": {
                    **{
                        "drawMode": {
                            "oneOf": DrawMode.__subclasses__()
                        },
                        "colorMode": {
                            "oneOf": ColorMode.__subclasses__()
                        },
                        "colors": {
                            "oneOf": [
                                {
                                    "type": "array",
                                    "items": FloatColor
                                },
                                FloatColor.getSubcolors
                            ]
                        },
                        "color": {
                            "type": "string",
                            "description": "Hex color",
                            "pattern": "^#[a-f0-9A-F]{6}|^#[a-f0-9A-F]{8}"
                        },
                        "getSubcolors": cls.getObjectDefinition(FloatColor.getSubcolors)
                    },
                    **{
                        x.__name__: cls.getObjectDefinition(x) for x in ColorMode.__subclasses__()
                    },
                    **{
                        x.__name__: cls.getObjectDefinition(x) for x in DrawMode.__subclasses__()
                    }
                },
            }

            # Replace all type references with the correct lookups
            cls._replaceTypes(schema)

            json.dump(schema, stream, indent=4)

    @classmethod
    def _replaceTypes(cls, input:dict|list):
        if isinstance(input, list):
            for i in range(len(input)):
                reference = cls._getReference(input[i])
                if reference != None:
                    input[i] = reference
                else:
                    cls._replaceTypes(input[i])
        elif isinstance(input, dict):
            for k, v in input.items():
                reference = cls._getReference(v)
                if reference != None:
                    input[k] = reference
                else:
                    cls._replaceTypes(v)

    @classmethod
    def getObjectDefinition(cls, input:type|function) -> dict:
        if isinstance(input, type):
            constructorSpec = inspect.getfullargspec(input.__init__)
            return {
                "type": "object",
                "required": [input.__name__],
                "properties": {
                    input.__name__: {
                        "type": "object",
                        "properties": {
                            k: v for k,v in constructorSpec.annotations.items()
                        },
                        "required": [
                            k for k,v in constructorSpec.annotations.items()
                        ]
                    }
                }
            }

        if callable(input):
            functionSpec = inspect.signature(input, eval_str=True)
            return {
                "type": "object",
                "required": [input.__name__],
                "properties": {
                    input.__name__: {
                        "type": "object",
                        "properties": {
                            k: v.annotation for k,v in functionSpec.parameters.items()
                        },
                        "required": [
                            k for k,v in functionSpec.parameters.items()
                        ]
                    }
                }
            }

    @classmethod
    def _getReference(cls, input) -> dict | None:
        if isinstance(input, type):
            if issubclass(input, ColorMode) and input != ColorMode:
                return {"$ref": f"#/$defs/{input.__name__}"}
            if issubclass(input, DrawMode) and input != DrawMode:
                return {"$ref": f"#/$defs/{input.__name__}"}
            if input == FloatColor:
                return {"$ref": "#/$defs/color"}
            elif input == list[FloatColor]:
                return {"$ref": "#/$defs/colors"}
            elif input == ColorMode:
                return {"$ref": "#/$defs/colorMode"}
            elif input == DrawMode:
                return {"$ref": "#/$defs/drawMode"}
            elif input == int:
                return {"type": "number"}
            elif input == float:
                return {"type": "number"}

        if input == FloatColor.getSubcolors:
            return { "$ref": "#/$defs/getSubcolors" }

        return None

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    if arguments['generate']:
        SchemaGenerator.generate()
    else:
        logging.basicConfig(level=logging.DEBUG)
        window = DrawUI()
        window.mainloop()

if __name__ == '__main__':
    main()
