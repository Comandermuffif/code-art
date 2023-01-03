from abc import abstractmethod

from models import FloatColor

class DrawMode(object):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_option_types(self) -> dict[str, tuple[str, type, object]]:
        pass

    @abstractmethod
    def draw(self, colors:list[FloatColor], *args, **kwargs):
        pass