from __future__ import annotations

from math import atan2, dist
import math

class FloatColor():
    def __init__(self, r:float, g:float, b:float, a:float=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def toHex(self):
        hex(int(self.g * 255))
        return "#{:02x}{:02x}{:02x}{:02x}".format(int(self.r * 255), int(self.g * 255), int(self.b * 255), int(self.a * 255)).upper()

    def toTuple(self) -> tuple[float, float, float, float]:
        return (self.r, self.g, self.b, self.a)

    def inverted(self):
        return FloatColor(1 - self.r, 1 - self.g, 1 - self.b)

    def __repr__(self) -> str:
        return self.toHex()

    def __add__(self, other:FloatColor):
        return FloatColor(
            self.r + other.r,
            self.g + other.g,
            self.b + other.b,
            self.a + other.a,
        )

    def __sub__(self, other:FloatColor):
        return FloatColor(
            self.r - other.r,
            self.g - other.g,
            self.b - other.b,
            self.a - other.a,
        )

    def __mul__(self, y:float):
        return FloatColor(
            self.r * y,
            self.g * y,
            self.b * y,
            self.a * y,
        )

    def __div__(self, y:float):
        return FloatColor(
            self.r / y,
            self.g / y,
            self.b / y,
            self.a / y,
        )

    @classmethod
    def fromHex(cls, input:str) -> FloatColor:
        input = input.strip().strip('#')
        if len(input) == 6:
            parts = tuple(int(input[i:i+2], 16) for i in (0, 2, 4))
            return FloatColor(parts[0]/255, parts[1]/255, parts[2]/255)
        elif len(input) == 8:
            parts = tuple(int(input[i:i+2], 16) for i in (0, 2, 4, 6))
            return FloatColor(parts[0]/255, parts[1]/255, parts[2]/255, parts[3]/255)
        else:
            return None

    @classmethod
    def fromHexList(cls, input:str) -> list[FloatColor]:
        return [
            cls.fromHex(x)
            for x in input.split(',')
        ]

    @classmethod
    def getSubcolors(cls, colors:list[FloatColor], subcount:int, wrap=False) -> list[FloatColor]:
        full_colors = list()

        # The steps between 0 and 1
        substeps = list([
            (s + 1)/(subcount + 1)
            for s in range(subcount)
        ])

        # For every color
        for i, current_color in enumerate(colors):
            # Add the current color
            full_colors.append(current_color)

            # Get the next color
            next_color = colors[(i + 1) % len(colors)]

            # Get the difference between the two colors
            color_delta = next_color - current_color

            # If this is the last color, and we're not wrapping
            if i == len(colors) - 1 and not wrap:
                # Stop
                continue

            # For every substep
            for substep in substeps:
                full_colors.append(current_color + (color_delta * substep))
        return full_colors

class Point(object):
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def distance(self, other:Point) -> float:
        return dist((self.x, self.y), (other.x, other.y))

    def get_angle(self, other:Point):
        shifted_point = other - self
        return atan2(shifted_point.y, shifted_point.x)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __eq__(self, other:Point) -> bool:
        if other is not Point:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point({self.x:0.3f},{self.y:0.3f})"

    def __add__(self, other:Point) -> Point:
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other:Point) -> Point:
        return Point(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, other:Point) -> Point:
        if isinstance(other, Point):
            return Point(
                self.x * other.x,
                self.y * other.y
            )
        else:
            return Point(self.x * other, self.y * other)

    def __truediv__(self, other:Point) -> Point:
        return self.__div__(other)

    def __div__(self, other:Point) -> Point:
        return Point(
            self.x / other.x,
            self.y / other.y
        )

    def __eq__(self, other: object) -> bool:
        if type(other) is Point:
            return self.x == other.x and self.y == other.y
        return False

    def rotateAround(self, other:Point, angleRad:float) -> Point:
        return Point(
            math.cos(angleRad) * (self.x - other.x) - math.sin(angleRad) * (self.y - other.y) + other.x,
            math.sin(angleRad) * (self.x - other.x) + math.cos(angleRad) * (self.y - other.y) + other.y
        )