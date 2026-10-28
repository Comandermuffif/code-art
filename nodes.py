"""Code-art node library for the PyFlowGraph editor.

Each node is a small Python function (code-as-nodes). This module holds the
source for every color-mode and draw-mode node, generates the matching inline
GUI (widget) code, and can instantiate a node into a ``NodeGraph``.

The color-mode nodes build real ``color_modes`` objects and hand them downstream
by reference. The draw-mode nodes sample a color mode and render it with Qt into
a ``QImage`` shown in an inline preview.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Widget:
    """An inline GUI widget that feeds one function parameter."""
    param: str
    kind: str                  # "text" | "int" | "float"
    default: object
    minimum: float | None = None
    maximum: float | None = None


@dataclass
class NodeDef:
    """A single node type: its category, function source, and GUI widgets."""
    title: str
    category: str
    code: str
    widgets: list[Widget] = field(default_factory=list)
    show_output: bool = False  # render the returned QImage in an inline preview


# --- Code generation ---------------------------------------------------------

def _gui_code(node_def: NodeDef) -> str:
    lines: list[str] = []
    for w in node_def.widgets:
        name = w.param
        if w.kind == "text":
            lines.append(f"widgets[{name!r}] = QtWidgets.QLineEdit({w.default!r})")
        elif w.kind == "int":
            lo = int(w.minimum) if w.minimum is not None else 0
            hi = int(w.maximum) if w.maximum is not None else 100000
            lines.append(f"widgets[{name!r}] = QtWidgets.QSpinBox()")
            lines.append(f"widgets[{name!r}].setRange({lo}, {hi})")
            lines.append(f"widgets[{name!r}].setValue({int(w.default)})")
        elif w.kind == "float":
            lo = float(w.minimum) if w.minimum is not None else -100000.0
            hi = float(w.maximum) if w.maximum is not None else 100000.0
            lines.append(f"widgets[{name!r}] = QtWidgets.QDoubleSpinBox()")
            lines.append(f"widgets[{name!r}].setRange({lo}, {hi})")
            lines.append(f"widgets[{name!r}].setDecimals(3)")
            lines.append(f"widgets[{name!r}].setValue({float(w.default)})")
        lines.append(f"layout.addWidget(widgets[{name!r}])")

    if node_def.show_output:
        lines.append("widgets['preview'] = QtWidgets.QLabel()")
        lines.append("widgets['preview'].setMinimumSize(160, 160)")
        lines.append("from PySide6.QtCore import Qt")
        lines.append("widgets['preview'].setAlignment(Qt.AlignmentFlag.AlignCenter)")
        lines.append("layout.addWidget(widgets['preview'])")
    return "\n".join(lines)


def _getter_expr(w: Widget) -> str:
    if w.kind == "text":
        return f"widgets[{w.param!r}].text()"
    return f"widgets[{w.param!r}].value()"


def _values_code(node_def: NodeDef) -> str:
    """Build the gui_get_values_code: get_values / set_values / set_initial_state."""
    get_entries = ", ".join(f"{w.param!r}: {_getter_expr(w)}" for w in node_def.widgets)
    get_body = "def get_values(widgets):\n    return {" + get_entries + "}\n"

    set_lines = ["def set_values(widgets, outputs):"]
    if node_def.show_output:
        set_lines += [
            "    img = outputs.get('image')",
            "    preview = widgets.get('preview')",
            "    if img is not None and preview is not None:",
            "        from PySide6.QtGui import QPixmap",
            "        from PySide6.QtCore import Qt",
            "        pix = QPixmap.fromImage(img)",
            "        preview.setPixmap(pix.scaled(preview.size(),",
            "            Qt.AspectRatioMode.KeepAspectRatio,",
            "            Qt.TransformationMode.SmoothTransformation))",
        ]
    else:
        set_lines.append("    pass")
    set_body = "\n".join(set_lines) + "\n"

    init_lines = ["def set_initial_state(widgets, state):"]
    for w in node_def.widgets:
        if w.kind == "text":
            init_lines.append(
                f"    if {w.param!r} in state: widgets[{w.param!r}].setText(state[{w.param!r}])")
        else:
            init_lines.append(
                f"    if {w.param!r} in state: widgets[{w.param!r}].setValue(state[{w.param!r}])")
    if len(init_lines) == 1:
        init_lines.append("    pass")
    init_body = "\n".join(init_lines) + "\n"

    return get_body + "\n" + set_body + "\n" + init_body


# --- Node definitions --------------------------------------------------------

# Color-mode source nodes (leaf: no color input).
GRADIENT = NodeDef(
    title="Gradient", category="Color",
    code='''@node_entry
def gradient(colors: str = "#ff0000,#00ff00,#0000ff,#ff0000", orientation: int = 0) -> "ColorMode":
    from models import FloatColor
    from color_modes.gradient import GradientColorMode
    return GradientColorMode(FloatColor.fromHexList(colors), orientation)
''',
    widgets=[
        Widget("colors", "text", "#ff0000,#00ff00,#0000ff,#ff0000"),
        Widget("orientation", "int", 0, 0, 2),
    ],
)

GRID = NodeDef(
    title="Grid", category="Color",
    code='''@node_entry
def grid(colors: str = "#ff0000,#00ff00,#0000ff,#ffff00") -> "ColorMode":
    from models import FloatColor
    from color_modes.grid import GridColorMode
    return GridColorMode(FloatColor.fromHexList(colors))
''',
    widgets=[Widget("colors", "text", "#ff0000,#00ff00,#0000ff,#ffff00")],
)

RANDOM = NodeDef(
    title="Random", category="Color",
    code='''@node_entry
def random(colors: str = "#ff0000,#00ff00,#0000ff") -> "ColorMode":
    from models import FloatColor
    from color_modes.random import RandomColorMode
    return RandomColorMode(FloatColor.fromHexList(colors))
''',
    widgets=[Widget("colors", "text", "#ff0000,#00ff00,#0000ff")],
)

ARC = NodeDef(
    title="Arc", category="Color",
    code='''@node_entry
def arc(colors: str = "#ff0000,#00ff00,#0000ff,#ffff00,#00ffff") -> "ColorMode":
    from models import FloatColor
    from color_modes.arc import ArcColorMode
    return ArcColorMode(FloatColor.fromHexList(colors))
''',
    widgets=[Widget("colors", "text", "#ff0000,#00ff00,#0000ff,#ffff00,#00ffff")],
)

LINEAR_GRADIENT = NodeDef(
    title="Linear Gradient", category="Color",
    code='''@node_entry
def linear_gradient() -> "ColorMode":
    from color_modes.linear_gradient import LinearGradientColorMode
    return LinearGradientColorMode()
''',
)


# Color-mode modifier nodes (one child color input).
CLAMP = NodeDef(
    title="Clamp", category="Color Modifier",
    code='''@node_entry
def clamp(child: "ColorMode" = None, threshold: float = 0.5) -> "ColorMode":
    from color_modes.modify.clamp import ClampColorMode
    return ClampColorMode(child, threshold)
''',
    widgets=[Widget("threshold", "float", 0.5, 0.0, 1.0)],
)

INVERT = NodeDef(
    title="Invert", category="Color Modifier",
    code='''@node_entry
def invert(child: "ColorMode" = None) -> "ColorMode":
    from color_modes.modify.invert import InvertColorMode
    return InvertColorMode(child)
''',
)

TRANSFORM = NodeDef(
    title="Transform", category="Color Modifier",
    code='''@node_entry
def transform(child: "ColorMode" = None, x_offset: float = 0, y_offset: float = 0, x_scale: float = 1, y_scale: float = 1, angle_deg: float = 0) -> "ColorMode":
    from color_modes.modify.transform import TransformColorMode
    return TransformColorMode(child, x_offset, y_offset, x_scale, y_scale, angle_deg)
''',
    widgets=[
        Widget("x_offset", "float", 0.0, -1.0, 1.0),
        Widget("y_offset", "float", 0.0, -1.0, 1.0),
        Widget("x_scale", "float", 1.0, 0.0, 4.0),
        Widget("y_scale", "float", 1.0, 0.0, 4.0),
        Widget("angle_deg", "float", 0.0, -360.0, 360.0),
    ],
)

GLOBE = NodeDef(
    title="Globe", category="Color Modifier",
    code='''@node_entry
def globe(child: "ColorMode" = None, x: float = 0.5, y: float = 0.5, radious: float = 0.4) -> "ColorMode":
    from color_modes.modify.globe import GlobeColorMode
    return GlobeColorMode(child, x, y, radious)
''',
    widgets=[
        Widget("x", "float", 0.5, 0.0, 1.0),
        Widget("y", "float", 0.5, 0.0, 1.0),
        Widget("radious", "float", 0.4, 0.0, 1.0),
    ],
)

NORMAL = NodeDef(
    title="Normal", category="Color Modifier",
    code='''@node_entry
def normal(child: "ColorMode" = None, x_divergence: float = 0.1, y_divergence: float = 0.1) -> "ColorMode":
    from color_modes.modify.normal import NormalColorMode
    return NormalColorMode(child, x_divergence, y_divergence)
''',
    widgets=[
        Widget("x_divergence", "float", 0.1, 0.0, 1.0),
        Widget("y_divergence", "float", 0.1, 0.0, 1.0),
    ],
)

VORONOI = NodeDef(
    title="Voronoi", category="Color Modifier",
    code='''@node_entry
def voronoi(child: "ColorMode" = None, count: int = 10) -> "ColorMode":
    from color_modes.modify.voronoi import VoronoiColorMode
    return VoronoiColorMode(child, count)
''',
    widgets=[Widget("count", "int", 10, 1, 200)],
)

AVG = NodeDef(
    title="Average", category="Color Modifier",
    code='''@node_entry
def avg(a: "ColorMode" = None, b: "ColorMode" = None) -> "ColorMode":
    from color_modes.modify.avg import AvgColorMode
    return AvgColorMode(a, b)
''',
)


# Draw-mode nodes (final: sample a color mode, render a QImage).
DRAW_CIRCLES = NodeDef(
    title="Draw Circles", category="Draw",
    code='''@node_entry
def circles(field: "ColorMode" = None, count: int = 300, min_size: float = 2, max_size: float = 20, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from render import render_to_qimage
    from render.circles import draw_circles
    return render_to_qimage(field, draw_circles, width, height, count=count, min_size=min_size, max_size=max_size)
''',
    widgets=[
        Widget("count", "int", 300, 1, 5000),
        Widget("min_size", "float", 2.0, 0.0, 200.0),
        Widget("max_size", "float", 20.0, 0.0, 200.0),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)

DRAW_SQUARES = NodeDef(
    title="Draw Squares", category="Draw",
    code='''@node_entry
def squares(field: "ColorMode" = None, count: int = 30, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from render import render_to_qimage
    from render.squares import draw_squares
    return render_to_qimage(field, draw_squares, width, height, count=count)
''',
    widgets=[
        Widget("count", "int", 30, 1, 500),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)

DRAW_TRIANGLES = NodeDef(
    title="Draw Triangles", category="Draw",
    code='''@node_entry
def triangles(field: "ColorMode" = None, count: int = 30, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from render import render_to_qimage
    from render.triangles import draw_triangles
    return render_to_qimage(field, draw_triangles, width, height, count=count)
''',
    widgets=[
        Widget("count", "int", 30, 1, 300),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)

DRAW_HEXAGON = NodeDef(
    title="Draw Hexagon", category="Draw",
    code='''@node_entry
def hexagon(field: "ColorMode" = None, count: int = 12, radious: float = 0.8, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from render import render_to_qimage
    from render.hexagon import draw_hexagon
    return render_to_qimage(field, draw_hexagon, width, height, count=count, radious=radious)
''',
    widgets=[
        Widget("count", "int", 12, 1, 100),
        Widget("radious", "float", 0.8, 0.0, 2.0),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)

DRAW_PATTERN = NodeDef(
    title="Draw Pattern", category="Draw",
    code='''@node_entry
def pattern(field: "ColorMode" = None, points: str = "0,0;1,0;0.5,1", count: int = 12, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from render import render_to_qimage
    from render.pattern import draw_pattern
    pts = [tuple(float(v) for v in pair.split(',')) for pair in points.split(';')]
    return render_to_qimage(field, draw_pattern, width, height, points=pts, count=count)
''',
    widgets=[
        Widget("points", "text", "0,0;1,0;0.5,1"),
        Widget("count", "int", 12, 1, 200),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)

DRAW_VORONOI = NodeDef(
    title="Draw Voronoi", category="Draw",
    code='''@node_entry
def voronoi_draw(field: "ColorMode" = None, count: int = 300, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from render import render_to_qimage
    from render.voronoi import draw_voronoi
    return render_to_qimage(field, draw_voronoi, width, height, count=count)
''',
    widgets=[
        Widget("count", "int", 300, 5, 5000),
        Widget("width", "int", 512, 16, 2048),
        Widget("height", "int", 512, 16, 2048),
    ],
    show_output=True,
)


NODE_DEFS: list[NodeDef] = [
    GRADIENT, GRID, RANDOM, ARC, LINEAR_GRADIENT,
    CLAMP, INVERT, TRANSFORM, GLOBE, NORMAL, VORONOI, AVG,
    DRAW_CIRCLES, DRAW_SQUARES, DRAW_TRIANGLES, DRAW_HEXAGON,
    DRAW_PATTERN, DRAW_VORONOI,
]


def node_defs_by_category() -> dict[str, list[NodeDef]]:
    """Group node definitions by category (menu order)."""
    grouped: dict[str, list[NodeDef]] = {}
    for nd in NODE_DEFS:
        grouped.setdefault(nd.category, []).append(nd)
    return grouped


def add_node(graph, node_def: NodeDef, pos=(0, 0)):
    """Instantiate a NodeDef into a NodeGraph (code + GUI + preview widgets)."""
    node = graph.create_node(node_def.title, pos=pos, use_command=False)
    node.set_code(node_def.code)
    node.set_gui_code(_gui_code(node_def))
    node.set_gui_get_values_code(_values_code(node_def))
    return node
