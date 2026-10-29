import unittest

from models import FloatColor


class FloatColorTests(unittest.TestCase):
    def test_subcolor(self):
        red = FloatColor(1, 0, 0)
        blue = FloatColor(0, 0, 1)

        colors = FloatColor.getSubcolors([red, blue], 1, False)
        self.assertEqual(3, len(colors))

        self.assertEqual(red, colors[0])
        self.assertEqual(FloatColor(0.5, 0, 0.5), colors[1])
        self.assertEqual(blue, colors[2])


    def test_wrap(self):
        red = FloatColor(1, 0, 0)
        blue = FloatColor(0, 0, 1)

        colors = FloatColor.getSubcolors([red, blue], 1, True)
        self.assertEqual(4, len(colors))

        self.assertEqual(red, colors[0])
        self.assertEqual(FloatColor(0.5, 0, 0.5), colors[1])
        self.assertEqual(blue, colors[2])
        self.assertEqual(FloatColor(0.5, 0, 0.5), colors[3])
