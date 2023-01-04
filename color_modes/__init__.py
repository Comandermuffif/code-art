from abc import abstractclassmethod, abstractmethod

from models import FloatColor

class ColorMode(object):
    @abstractclassmethod
    def get_name(self) -> str:
        pass

    @abstractclassmethod
    def get_option_types(self) -> dict[str, tuple[str, type, object]]:
        pass

    @abstractmethod
    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        pass

    @abstractmethod
    def get_color(self, x:float, y:float) -> FloatColor:
        pass