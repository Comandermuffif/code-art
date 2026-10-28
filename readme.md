# Code Art

A node-based generative-art editor. Build an image by wiring together
**color-mode** nodes (which produce a color field) and **draw-mode** nodes
(which sample a color field and paint it). The editor is built on
[PyFlowGraph](https://github.com/bhowiebkr/PyFlowGraph), a PySide6 node editor
where every node is a small Python function ("code as nodes").

Rendering uses Qt (`QPainter` / `QImage`); graphs are saved and loaded as
human-readable Markdown (`.md`).

## Setup

```sh
git clone --recursive <this-repo>
cd code-art
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you already cloned without `--recursive`, fetch the editor dependency with:

```sh
git submodule update --init --recursive
```

[PyFlowGraph](https://github.com/bhowiebkr/PyFlowGraph) (MIT licensed) is
included as a git submodule at `vendor/pyflowgraph`; the editor imports it from
`vendor/pyflowgraph/src`.

## Run

```sh
python app.py
```

- **Add nodes**: use the *Nodes* menu (grouped by category), or right-click the
  canvas → *Add Node*.
- **Wire nodes**: drag from an output pin (right) to an input pin (left). A node
  needs both a data connection (e.g. color field → draw node) and an execution
  connection (the thin exec pins) so it runs in order.
- **Execute**: press `F5` (or *Run → Execute Graph*). Draw nodes show the rendered
  image in an inline preview.
- **Save / Load**: *File → Save/Load* writes/reads a `.md` graph.

## Nodes

- **Color** sources: Gradient, Grid, Random, Arc, Linear Gradient. Each builds a
  real `ColorMode` object and passes it downstream by reference. Enter a
  palette as comma-separated hex (e.g. `#ff0000,#00ff00,#0000ff`).
- **Color Modifier**: Clamp, Invert, Transform, Globe, Normal, Voronoi, Average.
  These wrap a child color mode.
- **Draw**: Circles, Squares, Triangles, Hexagon, Pattern, Voronoi. Each samples
  its input color field and renders a `QImage` preview.
- **Output**: Save Image. Takes a draw node's `image` output and writes it to
  disk on execute — set the path in the widget or via *Browse...*; the format is
  inferred from the extension (`.png`, `.jpg`).

## Layout

- `app.py` — the editor window (embeds the PyFlowGraph scene/view).
- `nodes/` — the node library, one node per file:
  - `nodes/base.py` — shared `NodeDef`/`Widget` structures, GUI-code generation,
    and the `add_node` helper.
  - `nodes/color/` — color-source nodes (implementation + node definition in
    each file).
  - `nodes/modify/` — color-modifier nodes.
  - `nodes/draw/` — draw-mode nodes (QPainter ports of the old cairo draw
    modes) with `_render.py` holding the shared rendering helpers.
  - `nodes/output/` — output nodes (write the final image to disk).
- `models/` — shared data types (`FloatColor`, `Point`).
- `make_example.py` — writes a sample graph to `examples/demo.md`.
- `vendor/pyflowgraph/` — PyFlowGraph (git submodule).

## Contributing

```sh
python make_example.py   # regenerate examples/demo.md
```
