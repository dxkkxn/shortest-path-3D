#!/usr/bin/env python3
from linear_algebra import Point, Vector

def horner(poly, x):
    n = len(poly)
    res = poly[n - 1]
    i = 0
    for i in range(2, n+1):
        res = res * x + poly[n-i]
    return res

def cubic_bezier(points_list: list[Point]):
    polys = ((1, -3, 3, -1), (0, 3, -6, 3), (0, 0, 3, -3), (0, 0, 0, 1))
    print(points_list)
    assert(len(points_list) == len(polys))
    u = 0
    bezier_curve = []
    while u <= 1:
        res = Point(0, 0, 0)
        for poly, point in zip(polys, points_list):
            res_p = horner(poly, u)

            print(poly, u, res_p)
            x = res_p * point.x
            y = res_p * point.y
            z = res_p * point.z
            vec = Vector(Point(x, y, z))
            res = vec.translate(res)
        bezier_curve.append(res)
        u += 0.1
    # print(bezier_curve)
    return bezier_curve

M0 =Point(0, 1, 0)
M1 =Point(2, 5, 0)
M2 =Point(5, 4, 0)
M3 =Point(6, 0, 0)
print(cubic_bezier([M0, M1, M2, M3]))
# poly = (0, 0, 3, -3)
# x = 1
# print(horner(poly, x))
# print(-3*x**3 + 3*x**2)
