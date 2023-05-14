from math import floor
from random import choice

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

        for x in range(width):
            for y in range(width):
                # Randomly choose based on what's currently allowed
                color = choice(board.possible[x][y]).color
                board.grid[x][y] = color

                # Update neighbors
                for offset in cls.neighborOffsets:
                    # Skip checking elements off the board
                    if x + offset[0] > width - 1 or y + offset[1] > width - 1:
                        continue
                    if x + offset[0] < 0 or y + offset[1] < 0:
                        continue

                    # Don't reassign set neighbors
                    if board.grid[x + offset[0]][y + offset[1]] != None:
                        continue

                    possibleNeighbors = board.possible[x + offset[0]][y + offset[1]]
                    possibleNeighbors = [neighbor for neighbor in possibleNeighbors if color in neighbor.validNeighbors]
                    board.possible[x + offset[0]][y + offset[1]] = possibleNeighbors
        return board

class WaveFunctionCollapseColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor], boardWidth:int, boardHeight:int):
        self.board = WaveBoard.generate(boardWidth, boardHeight, [
            WaveNode(colors[x], [
                colors[(x-1) % len(colors)],
                colors[x],
                colors[(x+1) % len(colors)]
            ]) for x in range(len(colors))
        ])

    def getColor(self, x:float, y:float) -> FloatColor:
        x = floor(x * self.board.width) if x != 1 else self.board.width -1
        y = floor(y * self.board.height) if y != 1 else self.board.height -1

        return self.board.grid[x][y]
