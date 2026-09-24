"""
Класс вычислений/валидации — обёртка над логикой из Лабораторной работы №1.
"""
import logging
import math


class TriangleCalculator:
    """Вычисляет вид треугольника и координаты его вершин."""

    def calculate(self, str1, str2, str3):
        """
        Возвращает кортеж (tri_type, coords, error_message).

        tri_type: "равносторонний" | "равнобедренный" | "разносторонний" |
                   "не треугольник" | "" (нечисловые данные)
        coords: список из 3 кортежей (int, int)
        error_message: пустая строка при успехе, иначе описание ошибки
        """
        try:
            a = float(str1)
            b = float(str2)
            c = float(str3)
        except ValueError:
            logging.error("Некорректные входные данные: %r, %r, %r", str1, str2, str3)
            return "", [(-2, -2), (-2, -2), (-2, -2)], "Некорректные (нечисловые) входные данные"

        if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
            logging.warning("Треугольник с такими сторонами не существует: a=%s, b=%s, c=%s", a, b, c)
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], "Треугольник с такими сторонами не существует"

        if a == b == c:
            tri_type = "равносторонний"
        elif a == b or b == c or a == c:
            tri_type = "равнобедренный"
        else:
            tri_type = "разносторонний"

        x1, y1 = 0, 0
        x2, y2 = a, 0

        cos_theta = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        cos_theta = max(-1.0, min(1.0, cos_theta))
        theta = math.acos(cos_theta)

        x3 = c * math.cos(theta)
        y3 = c * math.sin(theta)

        points = [(x1, y1), (x2, y2), (x3, y3)]

        max_side = max(p[0] for p in points) - min(p[0] for p in points)
        max_side = max(max_side, max(p[1] for p in points) - min(p[1] for p in points))
        scale = 98 / max_side

        coords = [(int(px * scale) + 1, int(py * scale) + 1) for px, py in points]
        logging.info("Определён вид треугольника: %s, координаты: %s", tri_type, coords)

        return tri_type, coords, ""
