from abc import abstractmethod, abstractclassmethod

import cairo

from color_modes import ColorMode

class DrawMode(object):
    @abstractclassmethod
    def get_name(self):
        pass

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        pass