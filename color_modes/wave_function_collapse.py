from math import floor

from color_modes import ColorMode
from models import FloatColor
from models.wave_function_collapse import WaveBoard, WaveNode

# https://medium.com/swlh/wave-function-collapse-tutorial-with-a-basic-exmaple-implementation-in-python-152d83d5cdb1

class WaveFunctionCollapseColorMode(ColorMode):
    def __init__(self, colors:list[FloatColor], boardWidth:int, boardHeight:int, neighbors:list[int]=[-1,0,0,0,1]):
        self.board = WaveBoard.generate(boardWidth, boardHeight, [
            WaveNode(colors[x], [colors[(x + i) % len(colors)] for i in neighbors]) for x in range(len(colors))
        ])

    def getColor(self, x:float, y:float) -> FloatColor:
        x = floor(x * self.board.width) if x != 1 else self.board.width -1
        y = floor(y * self.board.height) if y != 1 else self.board.height -1

        return self.board.grid[x][y]
