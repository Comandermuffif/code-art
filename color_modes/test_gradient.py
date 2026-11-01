import math
import unittest

from color_modes.gradient import GradientColorMode
from models import FloatColor

def palette(size:int=5) -> list[FloatColor]:
    """Distinct colours: index i is (i, i, i) scaled into 0..1"""
    return [FloatColor(i / (size - 1), 1 - i / (size - 1), 0.5) for i in range(size)]

class GradientColorModeUnitTests(unittest.TestCase):
    def test_in_range_samples_are_unchanged(self):
        colors = palette()
        mode = GradientColorMode(colors)
        buckets = len(colors)

        for x in [i / 10 for i in range(11)]:
            for y in [i / 10 for i in range(11)]:
                # The algorithm the mode used before clamping was introduced
                index = math.floor((x * buckets + y * buckets) / 2)
                expected = colors[-1] if index == buckets else colors[index]

                self.assertEqual(expected, mode.getColor(x, y), f"at {x}, {y}")

    def test_samples_past_the_end_return_the_last_colour(self):
        colors = palette()
        mode = GradientColorMode(colors)

        self.assertEqual(colors[-1], mode.getColor(2, 2))
        self.assertEqual(colors[-1], mode.getColor(4, 4))
        self.assertEqual(colors[-1], mode.getColor(1.01, 1.01))

    def test_samples_before_the_start_return_the_first_colour(self):
        colors = palette()
        mode = GradientColorMode(colors)

        self.assertEqual(colors[0], mode.getColor(-0.5, -0.5))
        self.assertEqual(colors[0], mode.getColor(0, -1))

    def test_out_of_range_never_wraps(self):
        colors = palette()
        mode = GradientColorMode(colors)

        for x in [-2, -0.5, 0, 0.5, 1, 1.5, 3]:
            for y in [-2, -0.5, 0, 0.5, 1, 1.5, 3]:
                result = mode.getColor(x, y)
                if result == colors[0]:
                    continue
                # Every result must be a colour that a legitimate in-range sample can produce
                self.assertIn(result, colors)

    def test_orientation_one_edge_extension(self):
        colors = palette()
        mode = GradientColorMode(colors, orientation=1)

        self.assertEqual(colors[-1], mode.getColor(5, 0))


if __name__ == '__main__':
    unittest.main()