import unittest

from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions

from pages.calculator_page import CalculatorPage


class TestSimpleCalculator(unittest.TestCase):
    def setUp(self):
        self.driver = None
        self.addCleanup(self._quit_driver)

        options = SafariOptions()
        self.driver = webdriver.Safari(options=options)
        self.page = CalculatorPage(self.driver).open()

    def _quit_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass

    # ---------- сложение ----------
    def test_addition_positive_numbers(self):
        self.assertEqual(self.page.calculate(2, 3, "+"), "2 + 3 = 5")

    def test_addition_with_zero(self):
        self.assertEqual(self.page.calculate(0, 7, "+"), "0 + 7 = 7")

    # ---------- вычитание ----------
    def test_subtraction(self):
        self.assertEqual(self.page.calculate(10, 4, "-"), "10 - 4 = 6")

    def test_subtraction_negative_result(self):
        self.assertEqual(self.page.calculate(3, 8, "-"), "3 - 8 = -5")

    # ---------- умножение ----------
    def test_multiplication(self):
        self.assertEqual(self.page.calculate(6, 7, "*"), "6 * 7 = 42")

    def test_multiplication_by_zero(self):
        self.assertEqual(self.page.calculate(12345, 0, "*"), "12345 * 0 = 0")

    # ---------- деление ----------
    def test_division(self):
        self.assertEqual(self.page.calculate(20, 4, "/"), "20 / 4 = 5")

    def test_division_by_zero(self):
        result = self.page.calculate(5, 0, "/")
        self.assertEqual(result, "5 / 0 = null")

    # ---------- граничные значения ----------
    def test_large_numbers_addition(self):
        self.assertEqual(
            self.page.calculate(999999, 1, "+"),
            "999999 + 1 = 1000000",
        )

    def test_negative_numbers_multiplication(self):
        self.assertEqual(
            self.page.calculate(-3, 4, "*"),
            "-3 * 4 = -12",
        )


if __name__ == "__main__":
    unittest.main()