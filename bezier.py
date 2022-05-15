#!/usr/bin/env python3
from linear_algebra import Point, Vector


def cubic_bezier(points_list: list[Point]):
    """Compute a cubic bezier curve."""
    if not len(points_list) == 4:
        raise ValueError
    polys = ((1, -3, 3, -1), (0, 3, -6, 3), (0, 0, 3, -3), (0, 0, 0, 1))
    u = 0
    bezier_curve = []
    while u <= 1:
        res = Point(0, 0, 0)
        for poly, point in zip(polys, points_list):
            res_p = horner(poly, u)
            x = res_p * point.x
            y = res_p * point.y
            z = res_p * point.z
            vec = Vector(Point(x, y, z))
            res = vec.translate(res)
        bezier_curve.append(res)
        u += 0.1
    return bezier_curve


def horner(poly, x):
    """
    Horner algorithm implantantion.

    Ordered by degree
    """
    n = len(poly)
    res = poly[n - 1]
    i = 0
    for i in range(2, n + 1):
        res = res * x + poly[n - i]
    return res
