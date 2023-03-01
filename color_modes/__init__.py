from __future__ import annotations

from abc import abstractmethod
from models import FloatColor

class ColorMode():
    @abstractmethod
    def get_color(self, x:float, y:float) -> FloatColor:
        pass