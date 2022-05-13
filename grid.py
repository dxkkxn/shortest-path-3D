#!/usr/bin/env python3
import random
import copy
inf = float('inf')

class Grid(object):
    def __init__(self, size: int, seed: int):
        """Intialise the a grid of size size according the seed."""
        random.seed(seed)
        self.grid = [[random.randint(0, 255) for x in range(size)]
                     for x in range(size)]

    def __getitem__(self, key: tuple):
        """Retourne l'element designe par key."""
        # La key peut etre un tuple ou un entier
        if isinstance(key, tuple) and len(key) == 2:
            i, j = key
            if i >= len(self.grid):
                raise IndexError("First index out of range")
            if j >= len(self.grid[0]):
                raise IndexError("Seconde index out of range")
            return self.grid[i][j]

        elif (isinstance(key, int)):
            if key >= len(self.grid[0]):
                raise IndexError("First index out of range")
            return self.grid[key]
        else:
            raise ValueError("key type not valid only tuple and int")

    def __setitem__(self, key, val):
        """Mis a jour d'element designe par key."""
        assert(isinstance(val, float) or isinstance(val, int))
        if isinstance(key, tuple) and len(key) == 2:
            i, j = key
            if i >= len(self.grid):
                raise IndexError("First index out of range")
            if j >= len(self.grid[0]):
                raise IndexError("Seconde index out of range")
            self.grid[i][j] = val
        else:
            raise ValueError("key type not valid only tuple")

    def __str__(self):
        """Prints grid."""
        res = ""
        for i in range(len(self.grid)):
            res += str(self.grid[i])
            res += "\n"
        return res


    def __len__(self):
        """Return the lenght of grid."""
        return len(self.grid)

    def color(self, i, j):
        """Return color according the coord (i,j)."""
        color = self.old_grid[i][j]
        color = int(color)
        height = self.height(i, j)
        if height >= 8:
            # devrait etre une couleur blanchatre
            return color, color, color
        elif 8 > height >= 6.5:
            # brown = (151, 124, 83)
            mix = (151 + color) // 2, (124 + color) // 2, (83 + color) // 2
            return mix
        else:
            # green = (9, 176, 81)
            mix = (9 + color) // 2, (176 + color) // 2, (81 + color) // 2
            return mix

    def color_std(self, i, j):
        """Return the normalised color between 0..1."""
        color = self.color(i, j)
        return color[0] / 255, color[1] / 255, color[2] / 255

    def height(self, i, j):
        """Return the height of the coord (i,j)."""
        return self.old_grid[i][j] / 255 * 10

    def calculate_sense(self, p1, p2):
        """p1 --> p2."""
        i = p2[0] - p1[0]
        j = p2[1] - p1[1]
        if i == 1 and j == 1:
            return "rdiagonal down"
        if i == -1 and j == -1:
            return "rdiagonal up"

        if i == 1 and j == -1:
            return "ldiagonal down"
        if i == -1 and j == 1:
            print(p1, p2)
            return "ldiagonal up"

        if i == 0 and j == -1:
            return "horizontal left"
        if i == 0 and j == 1:
            return "horizontal right"

        if i == 1 and j == 0:
            return "vertical down"
        elif i == -1 and j == 0:
            return "vertical up"
        raise TypeError(f"p1 = {p1[0], p1[1]}, p2 = {p2[0], p2[1]}")
        return None

    def old(self, i, j):
        """Return old value of grid without infs."""
        return self.old_grid[i][j]

    def tuckey_smooth(self, radius: int):
        """Tuckey (median) smooth."""
        grid_copy = copy.deepcopy(self.grid)
        dep = [x for x in range(-radius, radius + 1)]
        length = len(self.grid)
        for i in range(length):
            for j in range(length):
                neigh = []
                for v in dep:
                    for h in dep:
                        if 0 <= i + v < length and 0 <= j + h < length:
                            neigh.append(self[i + v, j + h])
                neigh.sort()
                n = len(neigh)
                mid = n // 2
                if n % 2 == 0:
                    # pair
                    grid_copy[i] [j] = (neigh[mid] + neigh[mid + 1]) / 2
                else:
                    grid_copy[i][j] = neigh[mid]
        self.grid = grid_copy
        self.old_grid = copy.deepcopy(self.grid)

    def smooth(self, radius):
        """Average smooth."""
        grid_copy = copy.deepcopy(self.grid)
        dep = [x for x in range(-radius, radius + 1)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                neighbours = 0
                sum_neigh = 0
                for v in dep:
                    for h in dep:
                        if v != 0 and h != 0 and 0 <= i + v < len(self.grid) \
                        and 0 <= j + h < len(self.grid):
                            sum_neigh += self.grid[i + v][j + h]
                            neighbours += 1
                grid_copy[i][j] = sum_neigh / neighbours

        self.grid = grid_copy
        self.old_grid = copy.deepcopy(self.grid)
