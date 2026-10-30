"""Palette node: parse a comma-separated hex string into a list of colors.

The bridge between string palettes (easy to type) and the ``list[FloatColor]``
that color modes consume — downstream list nodes (Subset, Get Subcolors) can
modify the list before it reaches a color mode.
"""
from nodes.base import NodeDef, Widget


PALETTE = NodeDef(
    title="Palette", category="Palette",
    code='''@node_entry
def palette(hex_colors: str = "#ff0000,#00ff00,#0000ff,#ff0000") -> list[FloatColor]:
    """@outputs: colors"""
    from models import FloatColor
    return FloatColor.fromHexList(hex_colors)
''',
    widgets=[Widget("hex_colors", "text", "#ff0000,#00ff00,#0000ff,#ff0000")],
)
