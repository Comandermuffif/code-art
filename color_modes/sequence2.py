from color_modes import ColorMode
from models import FloatColor, StringSetting

class Sequence2ColorMode(ColorMode):
    def __init__(self):
        self.color = StringSetting("color", "Color", "ffffff,000000")
        self.mode = StringSetting("color", "Color", "ffffff,000000")
        super().__init__("Sequence2", [self.color, self.mode])
        self.index = 0

    def get_color(self, x: float, y: float) -> FloatColor:
        colors = [FloatColor.from_hex(x) for x in self.color.get().split(',')]

        if self.index > len(colors) - 1:
            self.index = 0
        return_color = colors[self.index]
        self.index += 1 

        return return_color