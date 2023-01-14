from color_modes import ColorMode
from models import FloatColor

class SequenceColorMode(ColorMode):
    @classmethod
    def get_name(cls) -> str:
        return "Sequence"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {}

    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        self.colors = colors
        self.current_index = 0

    def get_color(self, x:float, y:float) -> FloatColor:
        color = self.colors[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.colors)
        return color