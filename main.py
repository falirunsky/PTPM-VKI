import math


def get_triangle(str1, str2, str3):
    try:
        a = float(str1)
        b = float(str2)
        c = float(str3)
    except ValueError:
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        tri_type = "равносторонний"
    elif a == b or b == c or a == c:
        tri_type = "равнобедренный"
    else:
        tri_type = "разносторонний"

    x1, y1 = 0, 0
    x2, y2 = a, 0
    x3 = (c ** 2 - b ** 2 + a ** 2) / (2 * a)
    y3 = math.sqrt(max(c ** 2 - x3 ** 2, 0))

    points = [(x1, y1), (x2, y2), (x3, y3)]
    max_side = max(p[0] for p in points) - min(p[0] for p in points)
    max_side = max(max_side, max(p[1] for p in points) - min(p[1] for p in points))
    scale = 98 / max_side

    coords = [(int(px * scale) + 1, int(py * scale) + 1) for px, py in points]
    return tri_type, coords


if __name__ == "__main__":
    side1 = input("A: ")
    side2 = input("B: ")
    side3 = input("C: ")

    tri_type, coords = get_triangle(side1, side2, side3)
    print(tri_type)
    print(coords)