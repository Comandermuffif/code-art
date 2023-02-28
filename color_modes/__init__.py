from __future__ import annotations
from abc import abstractmethod

from models import FloatColor, Setting

class ColorMode(object):
    def __init__(self, name:str, settings:list[Setting]):
        self.name = name
        self.settings = settings

    @abstractmethod
    def get_color(self, x:float, y:float) -> FloatColor:
        pass

    def __repr__(self) -> str:
        return self.name