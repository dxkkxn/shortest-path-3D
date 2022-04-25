#!/usr/bin/env python3
"""Objets pour faire des operations en algebre linaire."""

class Point(object):
    """Class pour representer un point."""

    def __init__(self, x_coord, y_coord, z_coord):
        """Initialise les 3 coords d'un point."""
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord

    def __str__(self):
        """Representation en str."""
        return f"({self.x}, {self.y}, {self.z})"

    def to_tuple(self):
        """Renvoi le vector en forme de tuple."""
        return self.x, self.y, self.z

class Vector(object):
    """Class pour representer un vecteur et ses operations."""

    def __init__(self, a: Point, b: Point = None):
        """
        Creation d'un vecteur.

        Prends deux point p en 3D et le vector resultant est le vecteur
        allant des b vers a si b n'est pas saisi, b prens la valeur(0, 0, 0)
        """
        self.a = a
        if b is None:
            self.b = Point(0, 0, 0)
        else:
            self.b = b
        self.x = self.a.x-self.b.x
        self.y = self.a.y-self.b.y
        self.z = self.a.z-self.b.z

    def __sub__(self, v1):
        """Soustraction des 2 vecteurs."""
        return Vector(Point(self.x-v1.x, self.y-v1.y, self.z-v1.z))

    def __rmul__(self, scalar):
        """Multiplication par un scalaire."""
        assert(isinstance(scalar, float))
        return Vector(Point(scalar*self.x, scalar*self.y, scalar*self.z))

    def __add__(self, vector):
        """Addition des 2 vecteurs."""
        return Vector(Point(self.x+vector.x, self.y+vector.y, self.z+vector.z))

    def __str__(self):
        """Representation en str."""
        return f"({self.x}, {self.y}, {self.z})"

    def to_tuple(self):
        """Renvoi le vector en forme de tuple."""
        return self.x, self.y, self.z

    def __xor__(self, v):
        """Produit vectoriel des 2 vecteurs."""
        return Vector(Point(self.y*v.z - self.z*v.y,
                      self.z*v.x - self.x*v.z,
                      self.x*v.y - self.y*v.x))

    def translate(self, point: Point):
        """Translate d'un point avec le vecteur."""
        return Point(point.x+self.x, point.y+self.y, point.z+self.z)


class LineSegment(object):
    """Class pour representer un segment de droite."""

    def __init__(self, point_a: Point, point_b: Point):
        """Prends en entree deux points."""
        self.a = point_a
        self.b = point_b

    def mid_point(self):
        """Renvoi le milieu du segment."""
        v_a = Vector(self.a)
        v_b = Vector(self.b)

        sum_ = v_a + v_b
        return Point(sum_.x/2, sum_.y/2, sum_.z/2)


if __name__ == "__main__":
    v1 = Vector(10, 10, 10)
    v2 = Vector(1, 1, 1)
    print(v1 + v2)
