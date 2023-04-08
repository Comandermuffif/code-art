from __future__ import annotations

from math import atan2, dist

class DrawModes():
    random = "random"
    bucketed = "bucketed"
    gradient = "gradient"

class FloatColor():
    def __init__(self, r:float, g:float, b:float):
        self.r = r
        self.g = g
        self.b = b

    def to_hex(self):
        hex(int(self.g * 255))
        return "#{:02x}{:02x}{:02x}".format(int(self.r * 255), int(self.g * 255), int(self.b * 255)).upper()

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.r, self.g, self.b)

    def __repr__(self) -> str:
        return self.to_hex()

    def __add__(self, other:FloatColor):
        return FloatColor(
            self.r + other.r,
            self.g + other.g,
            self.b + other.b,
        )

    def __sub__(self, other:FloatColor):
        return FloatColor(
            self.r - other.r,
            self.g - other.g,
            self.b - other.b,
        )

    def __mul__(self, y:float):
        return FloatColor(
            self.r * y,
            self.g * y,
            self.b * y,
        )

    def __div__(self, y:float):
        return FloatColor(
            self.r / y,
            self.g / y,
            self.b / y,
        )

    @classmethod
    def from_hex(cls, input:str) -> FloatColor:
        input = input.strip().strip('#')
        parts = tuple(int(input[i:i+2], 16) for i in (0, 2, 4))
        return FloatColor(parts[0]/255, parts[1]/255, parts[2]/255)

    @classmethod
    def get_subcolors(cls, colors:list[FloatColor], subcount:int) -> list[FloatColor]:
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

class ColorPoint(Point):
    def __init__(self, x:float, y:float, color:FloatColor):
        super().__init__(x, y)
        self.color:FloatColor = color