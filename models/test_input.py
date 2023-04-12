import unittest

from models.input import ValueToken, parse, ArrayToken, FuncToken


class ParsingUnitTests(unittest.TestCase):
    def test_standard(self):
        result = parse("Voronoi(Gradient([fff100,ff8c00,e81123], 45))")
        self.assertIsInstance(result, FuncToken)
        result:FuncToken = result
        self.assertEqual("Voronoi", result.name)
        self.assertEqual(1, len(result.args))
        colorMode:FuncToken = result.args[0]
        self.assertEqual("Gradient", colorMode.name)
        self.assertEqual(2, len(colorMode.args))
        colors:ArrayToken = colorMode.args[0]
        self.assertEqual("45", colorMode.args[1].value)
        self.assertEqual(3, len(colors.values))
        self.assertEqual("fff100", colors.values[0].value)
        self.assertEqual("ff8c00", colors.values[1].value)
        self.assertEqual("e81123", colors.values[2].value)

    def test_array(self):
        result = parse("[fff100,ff8c00,e81123]")
        self.assertIsInstance(result, ArrayToken)
        result:ArrayToken = result
        self.assertEqual(3, len(result.values))

    def test_value(self):
        result = parse("fff100")
        self.assertIsInstance(result, ValueToken)
        result:ValueToken = result
        self.assertEqual("fff100", result.value)

    def test_function(self):
        result = parse("Voronoi(45)")
        self.assertIsInstance(result, FuncToken)
        result:FuncToken = result
        self.assertEqual("Voronoi", result.name)
        self.assertEqual(1, len(result.args))
        self.assertEqual("45", result.args[0].value)

