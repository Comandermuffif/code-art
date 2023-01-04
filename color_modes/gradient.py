from color_modes import ColorMode
from models import FloatColor

from utils.bucketed import BucketedUtils
from utils.gradient import GradientUtils

class GradientColorMode(ColorMode):
    @classmethod
    def get_name(self) -> str:
        return "Gradient"

    @classmethod
    def get_option_types(self) -> dict[str, tuple[str, type, object]]:
        return {
            'subcount': ("Subcount", int, 2),
            'divergance': ("Divergance", float, 0),
        }

    def __init__(self, colors:list[FloatColor], *args, **kwargs):
        self.subcount = int(kwargs["subcount"])
        self.divergance = float(kwargs["divergance"])
        self.full_colors = GradientUtils.get_subcolors(colors, self.subcount)

    def get_color(self, x:float, y:float) -> FloatColor:
        return BucketedUtils.get_color(x, y, self.full_colors, self.divergance)