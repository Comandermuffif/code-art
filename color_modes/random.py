import random

from color_modes import ColorMode
from models import FloatColor

class RandomColorMode(ColorMode):
    @classmethod
    def get_name(cls) -> str:
        return "Random"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {}

    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        self.colors = colors

    def get_color(self, x:float, y:float) -> FloatColor:
        return random.choice(self.colors)