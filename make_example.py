"""Build and save a sample code-art graph to examples/demo.md.

Run with:  python make_example.py

Demonstrates one flow: a color mode through a modifier into a draw mode,
ending in a Save Image node that writes the result to disk.
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "vendor", "pyflowgraph", "src"))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from core.node_graph import NodeGraph
from data.flow_format import save_flow_file
import nodes as N


def wire(graph, source, source_out, target, target_in):
    graph.create_connection(
        source.get_pin_by_name(source_out),
        target.get_pin_by_name(target_in),
        use_command=False,
    )
    graph.create_connection(
        source.get_pin_by_name("exec_out"),
        target.get_pin_by_name("exec_in"),
        use_command=False,
    )


def main():
    app = QApplication(sys.argv)
    graph = NodeGraph()

    # Single flow: Linear Gradient -> Invert -> Circles -> Save Image.
    lin = N.add_node(graph, N.LINEAR_GRADIENT, pos=(-750, -150))
    inv = N.add_node(graph, N.INVERT, pos=(-500, -150))
    circ = N.add_node(graph, N.DRAW_CIRCLES, pos=(-250, -150))
    save = N.add_node(graph, N.SAVE_IMAGE, pos=(0, -150))
    save.gui_widgets["path"].setText("generated/demo.png")
    wire(graph, lin, "output_1", inv, "child")
    wire(graph, inv, "output_1", circ, "field")
    wire(graph, circ, "image", save, "image")

    out = os.path.join(_HERE, "examples", "demo.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    save_flow_file(out, graph.serialize(), title="code-art demo",
                   description="A generative-art flow ending in an image saved to disk.")
    print("wrote", out)


if __name__ == "__main__":
    main()
