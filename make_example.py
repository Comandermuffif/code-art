"""Build and save a sample code-art graph to examples/demo.md.

Run with:  python make_example.py

Demonstrates a color-mode chain feeding two draw-mode previews.
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

    # Chain 1: Linear Gradient -> Invert -> Circles.
    lin = N.add_node(graph, N.LINEAR_GRADIENT, pos=(-600, -300))
    inv = N.add_node(graph, N.INVERT, pos=(-350, -300))
    circ = N.add_node(graph, N.DRAW_CIRCLES, pos=(-80, -300))
    wire(graph, lin, "output_1", inv, "child")
    wire(graph, inv, "output_1", circ, "field")

    # Chain 2: Grid -> Hexagon.
    grid = N.add_node(graph, N.GRID, pos=(-600, 200))
    hexa = N.add_node(graph, N.DRAW_HEXAGON, pos=(-350, 200))
    wire(graph, grid, "output_1", hexa, "field")

    out = os.path.join(_HERE, "examples", "demo.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    save_flow_file(out, graph.serialize(), title="code-art demo",
                   description="Two generative-art chains built with code-art nodes.")
    print("wrote", out)


if __name__ == "__main__":
    main()
