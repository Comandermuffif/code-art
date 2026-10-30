"""Build and save a sample code-art graph to examples/demo.md.

Run with:  python make_example.py

Demonstrates one flow: a hex palette parsed into a color list, expanded with
Get Subcolors, fed through a color mode and modifier into a draw mode, and
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


def _pin(node, name, direction):
    pins = node.output_pins if direction == "output" else node.input_pins
    return next(p for p in pins if p.name == name)


def wire(graph, source, source_out, target, target_in):
    graph.create_connection(
        _pin(source, source_out, "output"),
        _pin(target, target_in, "input"),
        use_command=False,
    )
    graph.create_connection(
        _pin(source, "exec_out", "output"),
        _pin(target, "exec_in", "input"),
        use_command=False,
    )


def main():
    app = QApplication(sys.argv)
    graph = NodeGraph()

    # Single flow: Palette -> Get Subcolors -> Gradient -> Invert -> Circles -> Save Image.
    pal = N.add_node(graph, N.PALETTE, pos=(-1000, -150))
    sub = N.add_node(graph, N.GET_SUBCOLORS, pos=(-750, -150))
    grad = N.add_node(graph, N.GRADIENT, pos=(-500, -150))
    inv = N.add_node(graph, N.INVERT, pos=(-250, -150))
    circ = N.add_node(graph, N.DRAW_CIRCLES, pos=(0, -150))
    save = N.add_node(graph, N.SAVE_IMAGE, pos=(250, -150))
    save.gui_widgets["path"].setText("generated/demo.png")
    wire(graph, pal, "colors", sub, "colors")
    wire(graph, sub, "colors", grad, "colors")
    wire(graph, grad, "output_1", inv, "child")
    wire(graph, inv, "output_1", circ, "field")
    wire(graph, circ, "image", save, "image")

    out = os.path.join(_HERE, "examples", "demo.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    save_flow_file(out, graph.serialize(), title="code-art demo",
                   description="A generative-art flow ending in an image saved to disk.")
    print("wrote", out)


if __name__ == "__main__":
    main()
