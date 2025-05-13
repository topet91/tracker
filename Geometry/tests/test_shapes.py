import unittest
from math import pi
from geometry_lib import Circle,Triangle,calculate_area


class TestCircle(unittest.TestCase):
    def test_area_calculation(self):
        circle = Circle(5)
        self.assertAlmostEqual(circle.area(), pi * 25, places=4)

    def test_invalid_radius(self):
        with self.assertRaises(ValueError):
            Circle(-1)


class TestTriangle(unittest.TestCase):
    def test_right_angle(self):
        triangle = Triangle(3, 4, 5)
        self.assertTrue(triangle.is_right_angle())

    def test_area_calculation(self):
        triangle = Triangle(5, 5, 6)
        self.assertAlmostEqual(triangle.area(), 12.0, places=4)

    def test_invalid_sides(self):
        with self.assertRaises(ValueError):
            Triangle(1, 2, 10)


class TestCalculateArea(unittest.TestCase):
    def test_polymorphism(self):
        shapes = [Circle(2), Triangle(3, 4, 5)]
        areas = [calculate_area(s) for s in shapes]
        self.assertAlmostEqual(areas[0], pi * 4)
        self.assertAlmostEqual(areas[1], 6.0)


if __name__ == "__main__":
    unittest.main()
