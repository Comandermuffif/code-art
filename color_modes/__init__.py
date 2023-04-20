from abc import abstractmethod

from models import FloatColor

class ColorMode(object):
    @abstractmethod
    def getColor(self, x:float, y:float) -> FloatColor:
        pass