import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from my_project import get_triangle


class TestTriangleType(unittest.TestCase):
    """Проверка корректности определения вида треугольника."""

    def test_equilateral_triangle_recognized(self):
        tri_type, _ = get_triangle("5", "5", "5")
        self.assertEqual(tri_type, "равносторонний")

    def test_isosceles_triangle_ab_equal(self):
        tri_type, _ = get_triangle("5", "5", "8")
        self.assertEqual(tri_type, "равнобедренный")

    def test_isosceles_triangle_bc_equal(self):
        tri_type, _ = get_triangle("8", "5", "5")
        self.assertEqual(tri_type, "равнобедренный")

    def test_isosceles_triangle_ac_equal(self):
        tri_type, _ = get_triangle("5", "8", "5")
        self.assertEqual(tri_type, "равнобедренный")

    def test_scalene_triangle_recognized(self):
        tri_type, _ = get_triangle("3", "4", "5")
        self.assertEqual(tri_type, "разносторонний")

    def test_scalene_triangle_with_floats(self):
        tri_type, _ = get_triangle("3.5", "4.2", "5.9")
        self.assertEqual(tri_type, "разносторонний")


class TestTriangleInequality(unittest.TestCase):
    """Проверка неравенства треугольника и вырожденных случаев."""

    def test_degenerate_sum_equal_third_side(self):
        tri_type, coords = get_triangle("1", "2", "3")
        self.assertEqual(tri_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_broken_inequality_a_side_too_long(self):
        tri_type, _ = get_triangle("100", "1", "1")
        self.assertEqual(tri_type, "не треугольник")

    def test_broken_inequality_b_side_too_long(self):
        tri_type, _ = get_triangle("1", "100", "1")
        self.assertEqual(tri_type, "не треугольник")

    def test_broken_inequality_c_side_too_long(self):
        tri_type, _ = get_triangle("1", "1", "100")
        self.assertEqual(tri_type, "не треугольник")

    def test_zero_side_length_is_not_triangle(self):
        tri_type, coords = get_triangle("0", "5", "5")
        self.assertEqual(tri_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_length_is_not_triangle(self):
        tri_type, coords = get_triangle("-3", "4", "5")
        self.assertEqual(tri_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_all_negative_sides_is_not_triangle(self):
        tri_type, _ = get_triangle("-3", "-4", "-5")
        self.assertEqual(tri_type, "не треугольник")


class TestTriangleInvalidInput(unittest.TestCase):
    """Проверка обработки некорректных (нечисловых) входных данных."""

    def test_non_numeric_first_argument_returns_empty_type(self):
        tri_type, coords = get_triangle("abc", "4", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_non_numeric_second_argument_returns_empty_type(self):
        tri_type, coords = get_triangle("3", "xyz", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_non_numeric_third_argument_returns_empty_type(self):
        tri_type, coords = get_triangle("3", "4", "five")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_string_argument_returns_empty_type(self):
        tri_type, coords = get_triangle("", "4", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_all_empty_strings_returns_empty_type(self):
        tri_type, coords = get_triangle("", "", "")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_special_characters_returns_empty_type(self):
        tri_type, coords = get_triangle("3", "4", "@#$")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_none_like_string_returns_empty_type(self):
        tri_type, coords = get_triangle("None", "4", "5")
        self.assertEqual(tri_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])


class TestTriangleCoordinates(unittest.TestCase):
    """Проверка формата и диапазона возвращаемых координат."""

    def test_coordinates_have_three_points(self):
        _, coords = get_triangle("3", "4", "5")
        self.assertEqual(len(coords), 3)

    def test_coordinates_are_int_tuples(self):
        _, coords = get_triangle("3", "4", "5")
        for point in coords:
            self.assertIsInstance(point, tuple)
            self.assertIsInstance(point[0], int)
            self.assertIsInstance(point[1], int)

    def test_coordinates_within_field_bounds(self):
        _, coords = get_triangle("3", "4", "5")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_coordinates_within_bounds_for_large_sides(self):
        _, coords = get_triangle("300", "400", "500")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_coordinates_within_bounds_for_equilateral(self):
        _, coords = get_triangle("10", "10", "10")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_first_vertex_is_origin_scaled(self):
        _, coords = get_triangle("3", "4", "5")
        self.assertEqual(coords[0], (1, 1))


class TestTriangleWhitespaceAndFormats(unittest.TestCase):
    """Проверка граничных форматов числовых строк."""

    def test_sides_with_surrounding_whitespace(self):
        tri_type, _ = get_triangle(" 5 ", " 5 ", " 5 ")
        self.assertEqual(tri_type, "равносторонний")

    def test_sides_with_leading_plus_sign(self):
        tri_type, _ = get_triangle("+5", "+5", "+5")
        self.assertEqual(tri_type, "равносторонний")

    def test_very_small_valid_sides(self):
        tri_type, _ = get_triangle("0.001", "0.001", "0.001")
        self.assertEqual(tri_type, "равносторонний")

    def test_scientific_notation_sides(self):
        tri_type, _ = get_triangle("1e2", "1e2", "1e2")
        self.assertEqual(tri_type, "равносторонний")


if __name__ == "__main__":
    unittest.main()
