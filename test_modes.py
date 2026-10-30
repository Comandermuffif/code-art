import ast
import sys
import unittest
from io import StringIO
from pathlib import Path

import color_modes
import draw_modes
from color_modes import ColorMode
from draw_modes import DrawMode
from models import FloatColor
from models.input import InputEvaluator, InputParser
from modes import colorModeClasses, discover, drawModeClasses, moduleNames

def declaredModes(package) -> set[str]:
    """Class names declared in the package's modules by parsing the sources.

    Reading the class declarations (rather than trusting sys.modules) means a
    brand new mode file is covered the moment it exists on disk.
    """
    root = Path(package.__file__).parent
    declared = set()

    for name in moduleNames(package):
        relative = name.split(".", 1)[1]
        path = root.joinpath(*relative.split(".")).with_suffix(".py")

        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.ClassDef):
                continue

            for base in node.bases:
                baseName = base.id if isinstance(base, ast.Name) else None
                if baseName in ("ColorMode", "DrawMode"):
                    declared.add(node.name)

    return declared


class ModeDiscoveryUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = discover()

    def test_test_modules_are_skipped(self):
        self.assertNotIn("color_modes.test_gradient", moduleNames(color_modes))

    def test_namespace_subpackages_are_walked(self):
        # color_modes/modify has no __init__.py, which pkgutil.walk_packages skips
        self.assertIn("color_modes.modify.invert", moduleNames(color_modes))
        self.assertIn("color_modes.modify.mask", moduleNames(color_modes))

    def test_every_module_is_imported(self):
        for name in moduleNames(color_modes) + moduleNames(draw_modes):
            self.assertIn(name, sys.modules, f"{name} was not imported")

    def test_every_declared_mode_registers_itself(self):
        registered = {mode.__name__ for mode in colorModeClasses() + drawModeClasses()}

        for package in (color_modes, draw_modes):
            missing = declaredModes(package) - registered
            self.assertFalse(missing, f"{package.__name__} modes not registered: {sorted(missing)}")

    def _evaluate(self, source:str) -> dict:
        captured = {}

        def SetColorMode(mode):
            captured["colorMode"] = mode

        def SetDrawMode(mode):
            captured["drawMode"] = mode

        def parseTypes(value:str):
            if value.startswith("#") and len(value) in (7, 9):
                return FloatColor.fromHex(value)

        evaluator = InputEvaluator(
            [SetColorMode, SetDrawMode, *drawModeClasses(), *colorModeClasses()],
            parseTypes,
        )
        evaluator.parse(InputParser.parse(StringIO(source)))
        return captured

    def test_modes_reachable_only_through_discovery(self):
        # Neither of these was imported by gui.py before discovery existed
        result = self._evaluate('SetColorMode(InvertColorMode(RandomColorMode(["#ff0000"])))')

        self.assertEqual("InvertColorMode", type(result["colorMode"]).__name__)
        self.assertEqual((0.0, 1.0, 1.0, 1.0), result["colorMode"].getColor(0.5, 0.5).toTuple())

        result = self._evaluate('SetColorMode(MaskColorMode(RandomColorMode(["#ff0000"]), RandomColorMode(["#00ff00"])))')

        self.assertEqual("MaskColorMode", type(result["colorMode"]).__name__)

    def test_draw_modes_reachable_through_discovery(self):
        result = self._evaluate("SetDrawMode(HexagonDrawMode(10))")

        self.assertEqual("HexagonDrawMode", type(result["drawMode"]).__name__)


if __name__ == '__main__':
    unittest.main()