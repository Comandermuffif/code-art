from math import floor
from random import choice, shuffle, randint

import itertools

from color_modes import ColorMode
from models import FloatColor

class WaveNode():
    def __init__(self, color: FloatColor, validNeighbors: list[FloatColor]):
        self.color = color
        self.validNeighbors = validNeighbors

class WaveBoard():
    neighborOffsets:list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height

        self.possible:list[list[list[WaveNode]]] = list(list(None for _ in range(height)) for _ in range(width))
        self.grid:list[list[FloatColor]] = list(list(None for _ in range(height)) for _ in range(width))

    @classmethod
    def generate(cls, width:int, height:int, nodes:list[WaveNode]):
        board = WaveBoard(width, height)

        # Fill the board so all things are possible
        for x in range(width):
            for y in range(width):
                board.possible[x][y] = nodes

        for (x, y) in itertools.product(range(width), range(height)):
            board.setCell(x, y)

        return board

    def setCell(self, x:int, y:int):
        color = choice(self.possible[x][y]).color
        self.grid[x][y] = color

        # Update neighbors
        for offset in self.neighborOffsets:
            # Skip checking elements off the board
            if x + offset[0] > self.width - 1 or y + offset[1] > self.width - 1:
                continue
            if x + offset[0] < 0 or y + offset[1] < 0:
                continue

            # Don't reassign set neighbors
            if self.grid[x + offset[0]][y + offset[1]] != None:
                continue

            possibleNeighbors = self.possible[x + offset[0]][y + offset[1]]
            possibleNeighbors = [neighbor for neighbor in possibleNeighbors if color in neighbor.validNeighbors]
            self.possible[x + offset[0]][y + offset[1]] = possibleNeighbors

class WaveFunctionCollapseColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor], boardWidth:int, boardHeight:int, neighbors:list[int]=[-1,0,0,0,1]):
        self.board = WaveBoard.generate(boardWidth, boardHeight, [
            WaveNode(colors[x], [colors[(x + i) % len(colors)] for i in neighbors]) for x in range(len(colors))
        ])

    def getColor(self, x:float, y:float) -> FloatColor:
        x = floor(x * self.board.width) if x != 1 else self.board.width -1
        y = floor(y * self.board.height) if y != 1 else self.board.height -1

        return self.board.grid[x][y]
