"""Shared building blocks for code-art node definitions.

Holds the data structures every node file uses (``Widget``, ``NodeDef``), the
``ColorMode`` base class, the GUI-code generators, and the ``add_node`` helper
that instantiates a ``NodeDef`` into a PyFlowGraph ``NodeGraph``.

This module is intentionally free of PySide6 imports and has no knowledge of
individual nodes — the ``nodes`` package discovers node files automatically.
"""
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field

from models import FloatColor


# --- Domain base -------------------------------------------------------------

class ColorMode(object):
    """A sampled color field: ``getColor(x, y)`` for x, y in [0, 1]."""
    @abstractmethod
    def getColor(self, x: float, y: float) -> FloatColor:
        pass


# --- Node definition structures ----------------------------------------------

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


# Menu ordering for node categories (unknown categories sort last).
CATEGORY_ORDER: list[str] = ["Color", "Palette", "Color Modifier", "Draw", "Composite", "Output"]


# --- Code generation ---------------------------------------------------------

def _gui_code(node_def: NodeDef) -> str:
    lines: list[str] = []
    for w in node_def.widgets:
        name = w.param
        if w.kind == "text":
            lines.append(f"widgets[{name!r}] = QtWidgets.QLineEdit({w.default!r})")
        elif w.kind == "bool":
            lines.append(f"widgets[{name!r}] = QtWidgets.QCheckBox({name!r})")
            lines.append(f"widgets[{name!r}].setChecked({bool(w.default)})")
        elif w.kind == "file":
            lines.append(f"widgets[{name!r}] = QtWidgets.QLineEdit({w.default!r})")
            lines.append(f"_row_{name} = QtWidgets.QHBoxLayout()")
            lines.append(f"_browse_btn_{name} = QtWidgets.QPushButton('Browse...')")
            lines.append(f"def _browse_pick_{name}():")
            lines.append("    from PySide6.QtWidgets import QFileDialog")
            lines.append(f"    picked, _ = QFileDialog.getSaveFileName(None, 'Save Image', widgets[{name!r}].text(), 'PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)')")
            lines.append(f"    if picked: widgets[{name!r}].setText(picked)")
            lines.append(f"_browse_btn_{name}.clicked.connect(_browse_pick_{name})")
            lines.append(f"_row_{name}.addWidget(widgets[{name!r}])")
            lines.append(f"_row_{name}.addWidget(_browse_btn_{name})")
            lines.append(f"layout.addLayout(_row_{name})")
            continue
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
    if w.kind in ("text", "file"):
        return f"widgets[{w.param!r}].text()"
    if w.kind == "bool":
        return f"widgets[{w.param!r}].isChecked()"
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
        if w.kind in ("text", "file"):
            init_lines.append(
                f"    if {w.param!r} in state: widgets[{w.param!r}].setText(state[{w.param!r}])")
        elif w.kind == "bool":
            init_lines.append(
                f"    if {w.param!r} in state: widgets[{w.param!r}].setChecked(bool(state[{w.param!r}]))")
        else:
            init_lines.append(
                f"    if {w.param!r} in state: widgets[{w.param!r}].setValue(state[{w.param!r}])")
    if len(init_lines) == 1:
        init_lines.append("    pass")
    init_body = "\n".join(init_lines) + "\n"

    return get_body + "\n" + set_body + "\n" + init_body


def finalize_node_gui(node) -> None:
    """Fix up a node's custom-widget GUI after it has been built.

    Two things PyFlowGraph's ``rebuild_gui`` doesn't handle for us:

    1. *Visibility/sizing.* The widgets live in a host embedded in the scene
       via a QGraphicsProxyWidget. When that host chain is already visible
       (a node added after a graph was loaded, or any deserialized node),
       Qt never sends the new widgets a Show event, the host layout reports a
       (0, 0) minimum, and the node collapses so its fields are clipped away.
       Show them explicitly and re-fit.

    2. *Styling.* On macOS the native widget style paints input fields via
       AppKit at fixed screen coordinates, so inside the proxy widget the
       white of an input box does not scale when the view zooms (and can
       render illegibly). Force Fusion — fully Qt-painted, scales with the
       scene transform like the rest of the node — and an explicit readable
       font, both set on the host so they propagate to every child widget.
    """
    host = node.custom_widget_host
    from PySide6.QtWidgets import QStyleFactory
    from PySide6.QtGui import QFont
    # Define a dark theme stylesheet for high contrast readability
    dark_style = "QWidget { background: transparent; color: #ffffff; }"
    dark_style += "QLineEdit, QSpinBox, QDoubleSpinBox { background-color: #3a3a3a; color: #ffffff; border: 1px solid #555555; border-radius: 3px; padding: 2px 4px; }"
    dark_style += "QCheckBox { color: #ffffff; }"
    dark_style += "QPushButton { background-color: #3a3a3a; color: #ffffff; border: 1px solid #555555; padding: 4px 8px; }"
    
    # setStyle takes ownership of the style object, so create a fresh one per
    # widget rather than sharing an instance.
    font = QFont("Arial", 10)
    # Set on the host and every widget explicitly: a child inherits its
    # parent's style only while it hasn't got one of its own, so relying on
    # propagation alone is fragile.
    host.setStyle(QStyleFactory.create("Fusion"))
    host.setFont(font)
    host.setStyleSheet(dark_style)
    for widget in node.gui_widgets.values():
        widget.setStyle(QStyleFactory.create("Fusion"))
        widget.setFont(font)
    for widget in node.gui_widgets.values():
        widget.show()
    node.custom_widget_layout.activate()
    node.fit_size_to_content()


def add_node(graph, node_def: NodeDef, pos=(0, 0)):
    """Instantiate a NodeDef into a NodeGraph (code + GUI + preview widgets)."""
    node = graph.create_node(node_def.title, pos=pos, use_command=False)
    # Annotations like `-> ColorMode` name types the executor namespace doesn't
    # define; the future import keeps them unevaluated while letting the
    # PyFlowGraph AST parser read them as real pin types (not "any").
    node.set_code("from __future__ import annotations\n\n" + node_def.code)
    node.set_gui_code(_gui_code(node_def))
    node.set_gui_get_values_code(_values_code(node_def))
    finalize_node_gui(node)
    return node
