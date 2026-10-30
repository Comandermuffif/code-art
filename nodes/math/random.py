"""Random node: Generate a random number
"""
from nodes.base import NodeDef, Widget


RANDOM = NodeDef(
    title="Random", category="Math",
    code='''@node_entry
def random(min:float, max:float) -> Tuple[float, int]:
    """@outputs: value, int_value"""
    from random import random
    value = random() * (max - min) + min
    return value, int(value)
''',
    widgets=[
        Widget("min", "float", 0.0),
        Widget("max", "float", 1.0),
    ],
)
