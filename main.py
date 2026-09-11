import logging
import math
import os
import sys


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
    ],
)


def get_triangle(str1, str2, str3):
    try:
        a = float(str1)
        b = float(str2)
        c = float(str3)
    except ValueError:
        logging.error("Некорректные входные данные: %r, %r, %r", str1, str2, str3)
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    logging.debug("Стороны: a=%s, b=%s, c=%s", a, b, c)

    if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
        logging.warning("Треугольник с такими сторонами не существует: a=%s, b=%s, c=%s", a, b, c)
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        tri_type = "равносторонний"
    elif a == b or b == c or a == c:
        tri_type = "равнобедренный"
    else:
        tri_type = "разносторонний"

    logging.info("Определён вид треугольника: %s", tri_type)

    x1, y1 = 0, 0
    x2, y2 = a, 0

    # b² = a² + c² - 2ac·cos(θ)  =>  cos(θ) = (a² + c² - b²) / (2ac)
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
    logging.info("Итоговые координаты: %s", coords)

    return tri_type, coords


if __name__ == "__main__":
    logging.info("Программа запущена")

    side1 = input("A: ")
    side2 = input("B: ")
    side3 = input("C: ")

    result_type, result_coords = get_triangle(side1, side2, side3)
    print(result_type)
    print(result_coords)