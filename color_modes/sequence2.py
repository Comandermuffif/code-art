from color_modes import ColorMode
from models import FloatColor, MultiChoiceSetting, StringSetting

class Sequence2ColorMode(ColorMode):
    def __init__(self):
        self.color = StringSetting("color", "Color: ", "ffffff,000000")
        self.mode = MultiChoiceSetting("mode", "Mode: ", 0, ["forward", "reverse"])
        super().__init__("Sequence2", [self.color, self.mode])
        self.index = 0

    def get_color(self, x: float, y: float) -> FloatColor:
        colors = [FloatColor.from_hex(x) for x in self.color.get().split(',')]

        if self.index > len(colors) - 1:
            self.index = 0
        if self.index < 0:
            self.index = len(colors) - 1

        return_color = colors[self.index]
        if self.mode.get() == "forward":
            self.index += 1
        else:
            self.index -= 1

        return return_color