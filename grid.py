#!/usr/bin/env python3
import random
import copy
inf = float('inf')

class Grid(object):
    def __init__(self, size: int, seed: int):
        random.seed(seed)
        self.grid = [[random.randint(0, 255) for x in range(size)]
                     for x in range(size)]
        # self.grid = tuckey_smooth(grid, 1)
        # self.old_grid = copy.deepcopy(grid)

    def __getitem__(self, key: tuple):
        assert(isinstance(key, tuple) and len(key) == 2)
        i, j = key
        return self.grid[i][j]
    def __setitem__(self, key: tuple, val):
        assert(isinstance(key, tuple) and len(key) == 2)
        i, j = key
        self.grid[i][j] = val
        return self.grid[i][j]


    def __len__(self):
        """Return the lenght of grid."""
        return len(self.grid)

    def color(self, i, j):
        """Calcul du color selon la coordonnee (i,j)."""
        color = self.old_grid[i][j]
        color = int(color)
        height = self.calculate_height(i, j)
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
        """Renvoie la color nomalise entre 0..1"""
        color = self.color(i, j)
        return color[0] / 255, color[1] / 255, color[2] / 255


    def calculate_height(self, i, j):
        """Calcul du hauteur selon la coordonnee (i,j)."""
        y = self.old_grid[i][j] / 255 * 10
        if y == inf:
            y = 0
        return y

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
        print(i, j)
        raise TypeError
        return None

    def tuckey_smooth(self, radius: int):
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

    def smooth(grid):
        grid_copy = copy.deepcopy(grid)
        dv = [-1, 0, 1]
        dh = [-1, 0, 1]
        for i in range(len(grid)):
            for j in range(len(grid)):
                neighbours = 0
                sum_neigh = 0
                for v in dv:
                    for h in dh:
                        if v != 0 and h != 0 and 0 <= i + v < len(grid) \
                        and 0 <= j + h < len(grid):
                            sum_neigh += grid[i + v][j + h]
                            neighbours += 1
                grid_copy[i][j] = sum_neigh / neighbours

        return grid_copy
