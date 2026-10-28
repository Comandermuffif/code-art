"""Subset node: take a slice of a color list (from main's ``subset``)."""
from nodes.base import NodeDef, Widget


SUBSET = NodeDef(
    title="Subset", category="Palette",
    code='''@node_entry
def subset(colors: list[FloatColor] = None, start: int = 0, end: int = -1) -> list[FloatColor]:
    """@outputs: colors"""
    if colors is None:
        raise ValueError("Subset: no color palette connected")
    if end < 0:
        return colors[start:]
    return colors[start:end]
''',
    widgets=[
        Widget("start", "int", 0, 0, 1000),
        Widget("end", "int", -1, -1, 1000),
    ],
)
