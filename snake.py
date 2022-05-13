#!/usr/bin/env python3
from linear_algebra import Point, Vector

class Snake():
    def __init__(self, size: int, pos_initial: Point):
        self.spheres = []
        self.distance = 10  # distance max between 2 sphere
        for _ in range(size):
            self.spheres.append(pos_initial)
        # head at index 0

    def move(self, point: Point):
        """Move the head of the snake to the position point."""
        new_position = [point]
        for i in range(1, len(self.spheres)):
            s_i_prime = new_position[-1]
            s_i_minus_one = self.spheres[i - 1]
            vec = Vector(s_i_minus_one, s_i_prime)
            if vec.norm() > self.distance:
                minus_d_u = -float(self.distance) * vec
                p = minus_d_u.translate(s_i_prime)
                if Vector(p, s_i_minus_one).norm() <= self.distance:
                    new_position.append(p)
                else:
                    new_position.append(self.spheres[i - 1])
            else:
                new_position.append(self.spheres[i - 1])
        self.spheres = new_position

    def get_positions(self):
        """Retourne les positions."""
        return self.spheres
