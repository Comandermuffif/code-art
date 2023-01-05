import random
import cairo

from color_modes import ColorMode
from draw_modes import DrawMode

class TextDrawMode(DrawMode):
    @classmethod
    def get_name(cls):
        return "Text"

    @classmethod
    def get_option_types(cls) -> dict[str, tuple[str, type, object]]:
        return {
            'count': ("Count", int, 500),
            'text': ("Text", str, "example"),
        }

    def __init__(self, *args, **kwargs):
        self.count = int(kwargs["count"])
        self.text = str(kwargs["text"])

    def draw(self, context:cairo.Context, color_mode:ColorMode, width:int, height:int) -> None:
        context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(13)
        
        for _ in range(self.count):
            x = random.randint(0, width)
            y = random.randint(0, height)

            context.move_to(x, y)
            color = color_mode.get_color(x/width, y/height)
            context.set_source_rgb(color.r, color.g, color.b)
            context.show_text(self.text)