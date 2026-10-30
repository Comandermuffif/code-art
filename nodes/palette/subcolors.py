"""Get Subcolors node: interpolate intermediate shades between palette colors.

Wraps ``FloatColor.getSubcolors`` from ``models`` (exposed as a helper in the
old text-DSL GUI on main).
"""
from nodes.base import NodeDef, Widget


GET_SUBCOLORS = NodeDef(
    title="Get Subcolors", category="Palette",
    code='''@node_entry
def subcolors(colors: list[FloatColor] = None, subcount: int = 4, wrap: bool = False) -> list[FloatColor]:
    """@outputs: colors"""
    from models import FloatColor
    if colors is None:
        raise ValueError("Get Subcolors: no color palette connected")
    return FloatColor.getSubcolors(colors, subcount, wrap)
''',
    widgets=[
        Widget("subcount", "int", 4, 0, 64),
        Widget("wrap", "bool", False),
    ],
)
