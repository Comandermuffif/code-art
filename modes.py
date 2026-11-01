"""Dynamic discovery of colour and draw modes.

Importing a module is what registers its classes as subclasses of ColorMode /
DrawMode, which is how InputEvaluator looks them up by name. Rather than adding
an import line to gui.py for every new mode, every module under color_modes/
and draw_modes/ is imported once here and picked up automatically.

Note: pkgutil.walk_packages() cannot be used here - it skips directories that
have no __init__.py (such as color_modes/modify/), silently losing modes.
"""
from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Type

import color_modes
import draw_modes
from color_modes import ColorMode
from draw_modes import DrawMode

PACKAGES = (color_modes, draw_modes)


def moduleNames(package) -> list[str]:
    """Names of every module inside a package, recursively.

    Test modules are skipped; helper modules are included so that a mode class
    can live in any file that is not a test.
    """
    root = Path(package.__file__).parent
    names = []
    for path in sorted(root.rglob("*.py")):
        parts = path.relative_to(root).with_suffix("").parts
        if parts[-1] == "__init__" or parts[-1].startswith("test"):
            continue
        names.append(".".join((package.__name__, *parts)))
    return names


def discover() -> list[str]:
    """Import every mode module once, registering its classes.

    Importing an already imported module is a no-op, so this can be called
    again safely. Modules that fail to import are logged and skipped so one
    broken mode does not take the whole interface down.
    """
    imported = []
    for package in PACKAGES:
        for name in moduleNames(package):
            try:
                importlib.import_module(name)
            except Exception:
                logging.exception("Unable to import mode module %s", name)
                continue
            imported.append(name)
    return imported


def colorModeClasses() -> list[Type[ColorMode]]:
    return ColorMode.__subclasses__()


def drawModeClasses() -> list[Type[DrawMode]]:
    return DrawMode.__subclasses__()
