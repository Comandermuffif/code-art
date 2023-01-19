from __future__ import annotations

from math import atan2, dist, radians, sqrt
from turtle import width

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

class Point(object):
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def distance(self, other:Point) -> float:
        return dist((self.x, self.y), (other.x, other.y))

    def get_angle(self, other:Point):
        shifted_point = other - self
        return atan2(shifted_point.y, shifted_point.x)

    @classmethod
    def get_circumcenter(cls, a:Point, b:Point, c:Point) -> Point:
        d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
        ux = ((a.x * a.x + a.y * a.y) * (b.y - c.y) + (b.x * b.x + b.y * b.y) * (c.y - a.y) + (c.x * c.x + c.y * c.y) * (a.y - b.y)) / d
        uy = ((a.x * a.x + a.y * a.y) * (c.x - b.x) + (b.x * b.x + b.y * b.y) * (a.x - c.x) + (c.x * c.x + c.y * c.y) * (b.x - a.x)) / d
        return Point(ux, uy)

    @classmethod
    def get_midpoint(cls, *points:Point) -> Point:
        return Point(
            (sum([p.x for p in points])) / (len(points)),
            (sum([p.y for p in points])) / (len(points)),
        )

    def __eq__(self, other:Point) -> bool:
        if other is not Point:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Point({self.x},{self.y})"

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

class Rect(object):
    def __init__(self, x:float, y:float, width:float, height:float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point:Point) -> bool:
        delta_x = point.x - self.x
        delta_y = point.y - self.y
        return delta_x > 0 and delta_x < self.width and delta_y > 0 and delta_y < self.height

    def corner_points(self) -> list[Point]:
        return [
            Point(self.x, self.y),
            Point(self.x + self.width, self.y),
            Point(self.x + self.width, self.y + self.height),
            Point(self.x, self.y + self.height),
        ]

    def subdivide(self) -> list[Rect]:
        return [
            Rect(self.x, self.y, self.width/2, self.height/2),
            Rect(self.x + self.width/2, self.y, self.width/2, self.height/2),
            Rect(self.x + self.width/2, self.y + self.height/2, self.width/2, self.height/2),
            Rect(self.x, self.y + self.height/2, self.width/2, self.height/2),
        ]

class ColorPoint(Point):
    def __init__(self, x:float, y:float, color:FloatColor):
        super().__init__(x, y)
        self.color:FloatColor = color

class Line(object):
    def __init__(self, point_a:Point, point_b:Point):
        self.point_a = point_a
        self.point_b = point_b

        self._y_slope = (point_b.x - point_a.x) / (point_b.y - point_a.y)
        self._x_slope = (point_b.y - point_a.y) / (point_b.x - point_a.x)

    def get_y(self, x:float) -> float:
        return (x - self.point_a.x) * self._x_slope + self.point_a.y

    def get_x(self, y:float) -> float:
        return (y - self.point_a.y) * self._y_slope + self.point_a.x

    def get_side(self, point:Point) -> int:
        d = (point.x - self.point_a.x) * (self.point_b.y - self.point_a.y) - (point.y - self.point_a.y) * (self.point_b.x - self.point_a.x)
        return d

    def get_distance(self, point:Point) -> float:
        return abs((self.point_b.x - self.point_a.x) * (self.point_a.y - point.y) - (self.point_a.x - point.x) * (self.point_b.y - self.point_a.y)) / sqrt(pow(self.point_b.x - self.point_a.x, 2) + pow(self.point_b.y - self.point_a.y, 2))

    def get_intersection(self, other:Line) -> Point | None:
        # Line self represented as a1x + b1y = c1
        a1 = self.point_b.y - self.point_a.y
        b1 = self.point_a.x - self.point_b.x
        c1 = a1 * (self.point_a.x) + b1 * (self.point_a.y)

        # Line other represented as a2x + b2y = c2
        a2 = other.point_b.y - other.point_a.y
        b2 = other.point_a.x - other.point_b.x
        c2 = a2 * (other.point_a.x) + b2 * (other.point_a.y)

        determinant = a1 * b2 - a2 * b1

        if (determinant == 0):
            return None
        else:
            x = (b2 * c1 - b1 * c2)/determinant
            y = (a1 * c2 - a2 * c1)/determinant
            return Point(x, y)

    @classmethod
    def get_decision_boundary(cls, point_a:Point, point_b:Point) -> Line:
        midpoint = (point_a + point_b) * Point(0.5, 0.5)
        delta = point_a - midpoint
        norm_a = midpoint + Point(delta.y, delta.x * -1)
        norm_b = midpoint - Point(delta.y, delta.x * -1)
        return Line(norm_a, norm_b)

    def limit(self, x_max:int, y_max:int, x_min=0, y_min=0) -> LineSegment:
        min_1 = self.get_x(y_min)
        min_2 = self.get_y(x_min)
        min_3 = self.get_x(x_max)
        min_4 = self.get_y(y_max)

        point_a = Point(x_min, min_2) if min_1 < 0 else Point(min_1, y_min)
        point_b = Point(x_max, min_3) if min_4 > x_max else Point(min_4, y_max)

        return LineSegment(point_a, point_b)

class LineSegment(Line):
    pass