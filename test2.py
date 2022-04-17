#!/usr/bin/env python3


class Vector(object):
    def __init__(self, x_coord, y_coord, z_coord):
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord
    def __sub__(self, v1):
        return Vector(self.x-v1.x, self.y-v1.y, self.z-v1.z)
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    def to_tuple(self):
        return self.x, self.y, self.z
    def __xor__(self, v):
        return Vector(self.y*v.z - self.z*v.y,
                      self.z*v.x - self.x*v.z,
                      self.x*v.y - self.y*v.x)
v = Vector(0, 1, 0)
v2 = Vector(1, 1, 0)
print(v, v2, v2-v, v2, v.to_tuple())
print(v ^ v2)
