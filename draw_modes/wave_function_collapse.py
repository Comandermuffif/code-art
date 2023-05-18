import cairo

from random import random
from scipy.spatial import Voronoi

from color_modes import ColorMode
from draw_modes import DrawMode
from models.wave_function_collapse import WaveBoard, WaveNode

class WaveFunctionCollapseDrawMode(DrawMode):
    def __init__(self, boardWidth:int, boardHeight:int, possibleNeighbors:list[int]=[-1,0,0,0,1]):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.possibleNeighbors = possibleNeighbors
        self.colorCount = 10

    def draw(self, context:cairo.Context, colorMode:ColorMode, width:int, height:int) -> None:
        colors = list([colorMode.getColor(random(), random()) for _ in range(self.colorCount)])

        board = WaveBoard.generate(self.boardWidth, self.boardHeight, [
            WaveNode(colors[j], [colors[(j + i) % len(colors)] for i in self.possibleNeighbors]) for j in range(len(colors))
        ])

        xStep = width / board.width
        yStep = height / board.height

        for x in range(board.width):
            for y in range(board.height):
                context.set_source_rgba(*board.grid[x][y].toTuple())
                context.rectangle(x * xStep, y * yStep, xStep, yStep)
                context.fill_preserve()
                context.stroke()