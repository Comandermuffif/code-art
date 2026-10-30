"""The code-art node library.

Each node lives in its own file under a category subfolder (``color/``,
``modify/``, ``draw/``) and holds both its implementation and its
``NodeDef``. Node files are discovered automatically: any module in this
package that defines a module-level ``NodeDef`` is registered, and its
variable name is exported here (so ``nodes.GRADIENT`` etc. keep working).
"""
from __future__ import annotations

import importlib
import pkgutil

from .base import (
    CATEGORY_ORDER,
    ColorMode,
    NodeDef,
    Widget,
    _getter_expr,
    _gui_code,
    _values_code,
    add_node,
    finalize_node_gui,
)

__all__ = [
    "ColorMode",
    "NodeDef",
    "NODE_DEFS",
    "Widget",
    "add_node",
    "finalize_node_gui",
    "node_defs_by_category",
    "CATEGORY_ORDER",
    "_gui_code",
    "_values_code",
]


def _discover() -> list[tuple[str, NodeDef]]:
    """Walk the package and collect every module-level NodeDef with its variable name."""
    found: list[tuple[str, NodeDef]] = []
    for info in pkgutil.walk_packages(__path__, prefix=__name__ + "."):
        if info.name.rsplit(".", 1)[-1].startswith("_"):
            continue
        module = importlib.import_module(info.name)
        for name, value in vars(module).items():
            if name.startswith("_"):
                continue
            if isinstance(value, NodeDef):
                found.append((name, value))
    return found


_FOUND: list[tuple[str, NodeDef]] = _discover()

NODE_DEFS: list[NodeDef] = [nd for _, nd in sorted(
    _FOUND,
    key=lambda pair: (
        CATEGORY_ORDER.index(pair[1].category) if pair[1].category in CATEGORY_ORDER else len(CATEGORY_ORDER),
        pair[1].title,
    ),
)]

# Export each NodeDef under its variable name (GRADIENT, DRAW_CIRCLES, ...).
for _name, _nd in _FOUND:
    globals()[_name] = _nd
del _name, _nd


def node_defs_by_category() -> dict[str, list[NodeDef]]:
    """Group node definitions by category, in menu order."""
    grouped: dict[str, list[NodeDef]] = {}
    for category in CATEGORY_ORDER:
        matches = [nd for nd in NODE_DEFS if nd.category == category]
        if matches:
            grouped[category] = matches
    # Any categories not in CATEGORY_ORDER (future-proofing).
    for nd in NODE_DEFS:
        if nd.category not in grouped:
            grouped[nd.category] = [x for x in NODE_DEFS if x.category == nd.category]
    return grouped
