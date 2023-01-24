import unittest

from models import Line, LineSegment, Point, Polygon

class TestLineMethods(unittest.TestCase):
    def test_get_x(self):
        # y = -1 + 2 * x
        # 1 = 2 * x + -1 * y
        point_a = Point(1, 1)
        point_b = Point(5, 9)

        for line in [Line(point_a, point_b), Line(point_b, point_a)]:
            with self.subTest(line=line):
                self.assertEqual(line.get_x(7), 4)
                self.assertEqual(line.get_x(0), 0.5)

                self.assertEqual(line.get_y(3), 5)
                self.assertEqual(line.get_y(5), 9)

    def test_horizontal_line(self):
        line = Line(
            Point(1, 3),
            Point(1, 7)
        )

        self.assertEqual(line.get_x(0), 1)
        self.assertEqual(line.get_y(0), None)

    def test_vertical_line(self):
        line = Line(
            Point(3, 1),
            Point(7, 1)
        )

        self.assertEqual(line.get_x(0), None)
        self.assertEqual(line.get_y(0), 1)

    def test_intersection(self):
        line_1 = Line(
            Point(3, 1),
            Point(7, 6)
        )

        line_2 = Line(
            Point(4, 6),
            Point(7, 2)
        )

        intersection = line_1.get_intersection(line_2)
        self.assertEqual(intersection.x, 169/31)
        self.assertEqual(intersection.y, 126/31)

    def test_limit(self):
        # 4 * y - 5 * x = -11
        line = Line(
            Point(3, 1),
            Point(7, 6)
        )

        line_segment = line.limit(10, 10)
        self.assertEqual(line_segment.point_a.x, 11/5)
        self.assertEqual(line_segment.point_a.y, 0)
        self.assertEqual(line_segment.point_b.x, 10)
        self.assertEqual(line_segment.point_b.y, 39/4)


class TestLineSegment(unittest.TestCase):
    def test_get_x(self):
        # 4 * y - 5 * x = -11
        line = LineSegment(
            Point(3, 1),
            Point(7, 6)
        )

        for (y, expected_x) in [(0, None), (5, 31/5), (10, None)]:
            with self.subTest(y=y, expected_x=expected_x):
                self.assertEqual(line.get_x(y), expected_x)

        for (x, expected_y) in [(0, None),(5, 7/2), (10, None)]:
            with self.subTest(x=x, expected_y=expected_y):
                self.assertEqual(line.get_y(x), expected_y)

    def test_limit(self):
        line_segment = Line(
            Point(0.7, 0.2),
            Point(0.4, 0.8),
        ).limit(1, 1)

        # Min
        # (0, 1.6)
        # (0.8, 0)
        # Max
        # (1, -0.4)
        # (0.3, 1)

        # (0.8, 0)
        # self.assertAlmostEqual(line_segment.point_a, Point(0.8, 0))
        self.assertAlmostEqual(line_segment.point_a.x, 0.8)
        self.assertAlmostEqual(line_segment.point_a.y, 0)
        # (0.3, 1)
        # self.assertAlmostEqual(line_segment.point_b, Point(0.3, 1))
        self.assertAlmostEqual(line_segment.point_b.x, 0.3)
        self.assertAlmostEqual(line_segment.point_b.y, 1)

class TestPolygon(unittest.TestCase):
    def test_from_segments(self):
        # Red
        boundaries_1 = [
            LineSegment(Point(0, 0.5), Point(1, 0.5)),
            LineSegment(Point(0.5, 0), Point(0.5, 1)),
        ]
        center_1 = Point(0.25, 0.25)
        polygon_1 = Polygon.from_segments(center_1, boundaries_1)

        self.assertEqual(len(polygon_1.points), 3)
        self.assertIn(Point(0.5, 0.5), polygon_1.points)
        self.assertIn(Point(0, 0.5), polygon_1.points)
        self.assertIn(Point(0.5, 0), polygon_1.points)

        # Blue
        boundaries_2 = [
            LineSegment(Point(0, 0.5), Point(1, 0.5)),
            LineSegment(Point(0, 0), Point(1, 1)),
        ]
        center_2 = Point(0.25, 0.75)
        polygon_2 = Polygon.from_segments(center_2, boundaries_2)

        self.assertEqual(len(polygon_2.points), 3)
        self.assertIn(Point(0, 0.5), polygon_2.points)
        self.assertIn(Point(0.5, 0.5), polygon_2.points)
        self.assertIn(Point(1, 1), polygon_2.points)

        # Green
        boundaries_3 = [
            LineSegment(Point(0.5, 0), Point(0.5, 1)),
            LineSegment(Point(0, 0), Point(1, 1)),
        ]
        center_3 = Point(0.75, 0.25)
        polygon_3 = Polygon.from_segments(center_3, boundaries_3)

        self.assertEqual(len(polygon_3.points), 3)
        self.assertIn(Point(0.5, 0), polygon_3.points)
        self.assertIn(Point(0.5, 0.5), polygon_3.points)
        self.assertIn(Point(1, 1), polygon_3.points)

if __name__ == '__main__':
    unittest.main()