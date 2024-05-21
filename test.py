import math

from models import Point

def getCenter(start:Point, offset:Point) -> Point:
    return start + Point(
        math.cos(math.radians(30)) * offset.x,
        -math.sin(math.radians(30)) * offset.x + offset.y,
    )

if __name__ == "__main__":
    origin = Point(0, 0)

    y = 0
    for x in range(4):
        center = getCenter(origin, Point(x, y))
        print(f"({x,y}) -> ({center.x},{center.y})")