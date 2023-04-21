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
    def getSubcolors(cls, colors:list[FloatColor], subcount:int) -> list[FloatColor]:
        full_colors = list()

        for i in range(len(colors) - 1):
            current_color = colors[i]
            full_colors.append(current_color)

            next_color = colors[i + 1]

            color_delta = next_color - current_color

            for j in range(subcount):
                full_colors.append(current_color + (color_delta * ((j + 1) / (subcount + 1))))

        full_colors.append(colors[-1])
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
        return Point(
            self.x * other.x,
            self.y * other.y
        )

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