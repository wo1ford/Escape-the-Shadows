import math


def lenght(x1, y1, x2, y2) -> float:
    a = (x1 - x2) ** 2
    b = (y1 - y2) ** 2
    c = math.sqrt(a + b)
    return c

