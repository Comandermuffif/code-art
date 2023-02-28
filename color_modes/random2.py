import random

from color_modes import ColorMode
from models import FloatColor, StringSetting

class Random2ColorMode(ColorMode):
    def __init__(self):
        self.color = StringSetting("color", "Color: ", "ffffff,000000")
        super().__init__("Random2", [self.color])
        self.index = 0

    def get_color(self, x: float, y: float) -> FloatColor:
        colors = [FloatColor.from_hex(x) for x in self.color.get().split(',')]
        return random.choice(colors)