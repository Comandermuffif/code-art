from __future__ import annotations
import itertools

from math import atan2, cos, dist, sin, sqrt

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

        # Line self represented as a * x + b * y = c
        self.a = self.point_b.y - self.point_a.y
        self.b = self.point_a.x - self.point_b.x
        self.c = self.a * (self.point_a.x) + self.b * (self.point_a.y)

    def __repr__(self) -> str:
        return f"Line<{self.point_a},{self.point_b}>"

    def get_y(self, x:float) -> float | None:
        if self.b == 0:
            # Line is only on one axis
            return None
        # (c - a * x) / b = y
        return (self.c - self.a * x) / self.b

    def get_x(self, y:float) -> float | None:
        if self.a == 0:
            # Line is only on one axis
            return None
        # x = (c - b * y) / a
        return (self.c - self.b * y) / self.a

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

    def get_closest(self, point:Point) -> Point:
        x1, y1 = self.point_a.as_tuple()
        x2, y2 = self.point_b.as_tuple()
        x3, y3 = point.as_tuple()
        dx, dy = x2-x1, y2-y1
        det = dx*dx + dy*dy
        a = (dy*(y3-y1)+dx*(x3-x1))/det

        return Point(x1+a*dx, y1+a*dy)

    @classmethod
    def get_decision_boundary(cls, point_a:Point, point_b:Point) -> Line:
        midpoint = (point_a + point_b) * Point(0.5, 0.5)
        delta = point_a - midpoint
        norm_a = midpoint + Point(delta.y, delta.x * -1)
        norm_b = midpoint - Point(delta.y, delta.x * -1)
        return Line(norm_a, norm_b)

    def limit(self, x_max:int, y_max:int, x_min=0, y_min=0) -> LineSegment:
        min_1 = Point(x_min, self.get_y(x_min))
        min_2 = Point(self.get_x(y_min), y_min)

        max_1 = Point(x_max, self.get_y(x_max))
        max_2 = Point(self.get_x(y_max), y_max)

        if min_1.y == None or min_1.y > y_max or min_1.y < y_min:
            point_a = min_2
        else:
            point_a = min_1

        if max_1.y == None or max_1.y > y_max or max_1.y < y_min:
            point_b = max_2
        else:
            point_b = max_1

        return LineSegment(point_a, point_b)

class LineSegment(Line):
    def get_x(self, y: float) -> float | None:
        x = super().get_x(y)
        if x < self.point_a.x and x < self.point_b.x:
            return None
        if x > self.point_a.x and x > self.point_b.x:
            return None
        return x

    def get_y(self, x: float) -> float | None:
        y = super().get_y(x)
        if y < self.point_a.y and y < self.point_b.y:
            return None
        if y > self.point_a.y and y > self.point_b.y:
            return None
        return y

    def get_intersection(self, other:LineSegment) -> Point | None:
        intersection = super().get_intersection(other)
        return intersection if self.contains(intersection) and other.contains(intersection) else None

    def contains(self, point:Point) -> bool:
        inside_x = (point.x >= self.point_a.x and point.x <= self.point_b.x) or (point.x >= self.point_b.x and point.x <= self.point_a.x)
        inside_y = (point.y >= self.point_a.y and point.y <= self.point_b.y) or (point.y >= self.point_b.y and point.y <= self.point_a.y)
        return inside_x and inside_y

    def get_nearest_end(self, point:Point):
        if point.distance(self.point_a) < point.distance(self.point_b):
            return self.point_a
        else:
            return self.point_b

    def get_farthest_end(self, point:Point):
        if point.distance(self.point_a) > point.distance(self.point_b):
            return self.point_a
        else:
            return self.point_b

    def get_midpoint(self) -> Point:
        return (self.point_a + self.point_b) * Point(0.5, 0.5)

class Ray(Line):
    def __init__(self, point:Point, angle_rad:float):
        super().__init__(point, point + Point(cos(angle_rad), sin(angle_rad)))
        self.angle_rad = angle_rad

class Polygon(object):
    def __init__(self):
        self.points = list[Point]()
        self.enclosed = None

    def get_center(self) -> Point:
        x = sum([p.x for p in self.points]) / len(self.points)
        y = sum([p.y for p in self.points]) / len(self.points)
        return Point(x, y)

    @classmethod
    def from_segments(cls, center:Point, boundaries:list[LineSegment], x_max:float=1, y_max:float=1) -> Polygon:
        sorted_lines = sorted([
            (center.get_angle(boundary_line.get_closest(center)), boundary_line)
            for boundary_line in boundaries
        ], key=lambda x: x[0])

        reduced_lines = [x[1] for x in sorted_lines]

        pass

        for index in range(len(reduced_lines)):
            line_1 = reduced_lines[index - 1]
            line_2 = reduced_lines[index]

            intersection_point = line_1.get_intersection(line_2)

            # If they don't intersect, skip
            if intersection_point == None:
                continue

            # If the intersection is not contained Skip it
            if not line_1.contains(intersection_point) or not line_2.contains(intersection_point):
                continue

            nearest_1 = line_1.get_closest(center)
            line_1_a = LineSegment(intersection_point, line_1.point_a)
            line_1_b = LineSegment(intersection_point, line_1.point_b)

            if line_1_a.contains(nearest_1) and line_1_b.contains(nearest_1):
                check_line = LineSegment(line_1_a.get_midpoint(), center)

                # If this new line segment is behind another line
                if check_line.get_intersection(line_2) != None:
                    reduced_lines[index - 1] = line_1_b
                else:
                    reduced_lines[index - 1] = line_1_a
            elif line_1_a.contains(nearest_1):
                reduced_lines[index - 1] = line_1_a
            elif line_1_b.contains(nearest_1):
                reduced_lines[index - 1] = line_1_b

            nearest_2 = line_2.get_closest(center)
            line_2_a = LineSegment(intersection_point, line_2.point_a)
            line_2_b = LineSegment(intersection_point, line_2.point_b)

            if line_2_a.contains(nearest_2) and line_2_b.contains(nearest_2):
                check_line = LineSegment(line_2_a.get_midpoint(), center)

                # If this new line segment is behind another line
                if check_line.get_intersection(line_1) != None:
                    reduced_lines[index] = line_2_b
                else:
                    reduced_lines[index] = line_2_a
            else:
                if line_2_a.contains(nearest_2):
                    reduced_lines[index] = line_2_a
                elif line_2_b.contains(nearest_2):
                    reduced_lines[index] = line_2_b

        known_points = set[Point]()
        unknown_points = set[Point]()

        # Generate the point list from the reduced lines
        for index in range(len(reduced_lines)):
            line_1 = reduced_lines[index - 1]
            line_2 = reduced_lines[index]

            # This is the intersection point
            if line_1.point_a == line_2.point_a or line_1.point_a == line_2.point_b:
                known_points.add(line_1.point_a)
                unknown_points.add(line_1.point_b)
            elif line_1.point_b == line_2.point_b or line_1.point_b == line_2.point_a:
                known_points.add(line_1.point_b)
                unknown_points.add(line_1.point_a)
            else:
                # The lines do not intersect, gonna need to add em all
                unknown_points.add(line_1.point_a)
                unknown_points.add(line_1.point_b)
                unknown_points.add(line_2.point_a)
                unknown_points.add(line_2.point_b)

        trailing_points = unknown_points - known_points

        # If the polygon isn't enclosed, check the trailing ends
        for unknown_point in trailing_points:
            known_points.add(unknown_point)

        missing_points = list(itertools.chain.from_iterable([
            (
                Point(p1.x, p2.y),
                Point(p2.x, p1.y),
            )
            for (p1, p2) in itertools.combinations(trailing_points, 2)
        ]))

        missing_points += [
            Point(0, 0),
            Point(0, y_max),
            Point(x_max, y_max),
            Point(x_max, 0)
        ]

        for missing_point in missing_points:
            if missing_point in known_points:
                continue

            check_line = LineSegment(missing_point, center)

            intersects = [
                boundary_line.get_intersection(check_line) != None
                for boundary_line in reduced_lines
            ]

            if not any(intersects):
                known_points.add(missing_point)

        sorted_points = sorted([
            (center.get_angle(p), p)
            for p in known_points
        ], key=lambda x: x[0])

        polygon = Polygon()
        polygon.enclosed = True if len(trailing_points) == 0 else False
        polygon.points = [x[1] for x in sorted_points]

        return polygon