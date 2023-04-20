from abc import abstractmethod

import cairo

from color_modes import ColorMode

class DrawMode(object):
    @abstractmethod
    def draw(self, context:cairo.Context, colorMode:ColorMode, width:int, height:int) -> None:
        pass