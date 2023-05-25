import itertools
import cairo

from random import choice, random

from color_modes import ColorMode
from draw_modes import DrawMode
from models import Colors, FloatColor

class Position:
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)

ALL_POSITIONS = [
            Position.UP,
            Position.LEFT,
            Position.DOWN,
            Position.RIGHT,
            Position.UP_LEFT,
            Position.UP_RIGHT,
            Position.DOWN_LEFT,
            Position.DOWN_RIGHT,
        ]

class Pattern(object):
    def __init__(self, colors:list[FloatColor]):
        """Constructor

        @colors: The 4 colors in (TL, TR, BL, BR)
        """
        if len(colors) != 4:
            raise ValueError("colors array must be 4")
        self.colors = colors

class Index(object):
    def __init__(self) -> None:
        self.data:dict[Pattern, dict[tuple[int, int], set[Pattern]]] = {}
        self.sealed = False

    def addPattern(self, pattern:Pattern) -> None:
        if self.sealed:
            raise IndexError("Index is sealed, new patterns cannot be added")
        self.data[pattern] = {}
        for position in ALL_POSITIONS:
            self.data[pattern][position] = set()

    def generate(self) -> None:
        self.sealed = True
        knownPatterns = list(self.data.keys())

        for (base, other) in itertools.permutations(knownPatterns, 2):
            for position in ALL_POSITIONS:
                if position == Position.LEFT:
                    valid = base.colors[0] == other.colors[1] and base.colors[2] == other.colors[3]
                elif position == Position.UP_LEFT:
                    valid = base.colors[0] == other.colors[3]
                elif position == Position.UP:
                    valid = base.colors[0] == other.colors[2] and base.colors[1] == other.colors[3]
                elif position == Position.UP_RIGHT:
                    valid = base.colors[1] == other.colors[2]
                elif position == Position.RIGHT:
                    valid = base.colors[1] == other.colors[0] and base.colors[3] == other.colors[2]
                elif position == Position.DOWN_RIGHT:
                    valid = base.colors[3] == other.colors[0]
                elif position == Position.DOWN:
                    valid = base.colors[2] == other.colors[0] and base.colors[3] == other.colors[1]
                elif position == Position.DOWN_LEFT:
                    valid = base.colors[2] == other.colors[1]
                else:
                    valid = False

                if valid:
                    self.data[base][position].add(other)

    def isPossible(self, base:Pattern, other:Pattern, position:tuple[int, int]) -> bool:
        if not self.sealed:
            raise IndexError("Index is not sealed, cannot check if possible")
        return other in self.data[base][position]

class Board(object):
    def __init__(self, width:int=5, height:int=5) -> None:
        self.width = width
        self.height = height

        self.possiblePatterns:list[list[list[Pattern]]] = list([
            list([
                list()
                for _ in range(height)
            ])
            for _ in range(width)
        ])

        self.colors:list[list[FloatColor]] =list([
            list([
                None
                for _ in range(height)
            ])
            for _ in range(width)
        ])
        self.index = Index()

    def _validDirs(self, x:int, y:int) -> list[tuple[int, int]]:
        validDirs = set(ALL_POSITIONS)
        if x == 0:
            validDirs -= Position.LEFT
            validDirs -= Position.UP_LEFT
            validDirs -= Position.DOWN_LEFT
        elif x == self.width - 1:
            validDirs -= Position.RIGHT
            validDirs -= Position.UP_RIGHT
            validDirs -= Position.DOWN_RIGHT
        if y == 0:
            validDirs -= Position.UP
            validDirs -= Position.UP_LEFT
            validDirs -= Position.UP_RIGHT
        elif y == self.height - 1:
            validDirs -= Position.DOWN
            validDirs -= Position.DOWN_LEFT
            validDirs -= Position.DOWN_RIGHT
        return validDirs


    def set(self, pattern:Pattern, x:int, y:int) -> None:
        self.colors[x][y] = pattern.colors[0]
        self.colors[x + 1][y] = pattern.colors[1]
        self.colors[x][y + 1] = pattern.colors[2]
        self.colors[x + 1][y + 1] = pattern.colors[3]

        # Update possible neighbors
        for (xRel, yRel) in self._validDirs(x, y):
            possiblePatterns = self.possiblePatterns[x + xRel][y + yRel]

    def generate(self, patterns:list[Pattern]) -> None:
        # Set all possible patterns
        for x in range(self.width):
            for y in range(self.height):
                self.possiblePatterns[x][y] = patterns

        for pattern in patterns:
            self.index.addPattern(pattern)
        self.index.generate()

        # Randomly pick the first pattern
        self.set(choice(self.possiblePatterns[0][0]), 0, 0)

        # Iterate through the board
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):

                newPossible = self.possiblePatterns[x][y]
                newPossible = [
                    pattern for pattern in newPossible
                    if pattern.colors[0] == self.colors[0] and pattern.colors[x] == self.colors[y]
                ]

                self.possiblePatterns[x][y] = newPossible

class WaveFunctionCollapseDrawMode(DrawMode):
    def __init__(self, boardWidth:int, boardHeight:int, possibleNeighbors:list[int]=[-1,0,0,0,1]):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.possibleNeighbors = possibleNeighbors
        self.colorCount = 10

    def draw(self, context:cairo.Context, colorMode:ColorMode, width:int, height:int) -> None:
        patterns = [
            Pattern([Colors.red, Colors.red, Colors.white, Colors.white]),
            Pattern([Colors.white, Colors.white, Colors.red, Colors.red]),
        ]

        board = Board()
        board.generate(patterns)

        xStep = width / board.width
        yStep = height / board.height

        for x in range(board.width):
            for y in range(board.height):
                color = board.colors[x][y]
                if color == None:
                    continue
                context.set_source_rgba(*color.toTuple())
                context.rectangle(x * xStep, y * yStep, xStep, yStep)
                context.fill_preserve()
                context.stroke()