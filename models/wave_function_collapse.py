from random import choice, shuffle, randint

import itertools

from models import FloatColor

class WaveNode():
    def __init__(self, color: FloatColor, weightedNeighbors: list[tuple[FloatColor, int]]):
        self.color = color
        self.weightedNeighbors = weightedNeighbors

class WaveBoard():
    neighborOffsets:list[tuple[int, int]] = [(0, -1), (0, 1), (-1, 0), (1, 0)]

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
        if len(self.possible[x][y]) == 0:
            raise RuntimeError("Impossible condition found")

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
            possibleNeighbors = [neighbor for neighbor in possibleNeighbors if color in neighbor.weightedNeighbors]
            self.possible[x + offset[0]][y + offset[1]] = possibleNeighbors
