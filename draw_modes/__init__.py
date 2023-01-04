from abc import abstractmethod, abstractclassmethod

import cairo

from color_modes import ColorMode
from models import FloatColor

class DrawMode(object):
    @abstractclassmethod
    def get_name(self):
        pass

    @abstractclassmethod
    def get_option_types(self) -> dict[str, tuple[str, type, object]]:
        pass

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        pass