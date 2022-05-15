import math
import heapq
from collections import deque
from sortedcontainers import SortedDict
import bisect

inf = float('inf')


def cost(grid, v1i: int, v1j: int, v2i: int, v2j: int):
    """Cost to go from v1 vertex to v2 vertex."""
    # we detect a diagonal mouvement
    if abs(v1i - v2i) and abs(v1j - v2j):
        weight = math.sqrt(2) * ((grid[v1i][v1j] + grid[v2i][v2j]) / 2)
    else:
        weight = (grid[v1i][v1j] + grid[v2i][v2j]) / 2
    return weight


def get_path(prev: dict, start: tuple, target: tuple):
    """Get path of vertexes going from start to target using prev dict."""
    curr_node = target
    path = [target]
    while curr_node != start:
        path.append(prev[curr_node])
        curr_node = prev[curr_node]
    path.reverse()
    return path


def check_neighbours_sd(grid, i: int, j: int, weight: dict,
                        sorted_weight: SortedDict, prev: dict, mark: set):
    """
    Check neighbours using sorted dict.

    for each neighbour of i, j if a new path is found update the parameters
    (weight, sorted_weight, prev, mark)
    """
    len_l = len(grid)
    len_c = len(grid[0])
    dep = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
           (1, 1)]
    for v, h in dep:
        ni, nj = i + v, j + h  # neighbour (ni, nj)
        if 0 <= ni < len_l and 0 <= nj < len_c and (ni, nj) not in mark:
            curr_weight = weight[i, j] + cost(grid, i, j, ni, nj)
            old_w = weight[ni, nj]
            if curr_weight < old_w:
                if curr_weight not in sorted_weight:
                    sorted_weight[curr_weight] = set([(ni, nj), ])
                else:
                    sorted_weight[curr_weight].add((ni, nj))
                weight[ni, nj] = curr_weight
                v_set = sorted_weight[old_w]
                v_set.remove((ni, nj))
                if len(v_set) == 0:
                    sorted_weight.pop(old_w)
                prev[(ni, nj)] = (i, j)
    return


def check_neighbours(grid, i: int, j: int, weight: dict, weight_heap: list,
                     prev: dict, mark: dict):
    """
    Check neighbours.

    for each neighbour of i, j if a new path is found update the parameters
    (weight, weight_heap, prev, mark)
    """
    len_l = len(grid)
    len_c = len(grid[0])
    dep = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
           (1, 1)]
    for v, h in dep:
        ni, nj = i + v, j + h  # neighbour (ni, nj)
        if 0 <= ni < len_l and 0 <= nj < len_c and (ni, nj) not in mark:
            curr_weight = weight[i, j] + cost(grid, i, j, ni, nj)
            if curr_weight < weight[ni, nj]:
                heapq.heappush(weight_heap, (curr_weight, (ni, nj)))
                weight[(ni, nj)] = curr_weight
                prev[(ni, nj)] = (i, j)
    return


def check_neighbours_dq(grid, i: int, j: int, weight: dict,
                        weight_dq: deque, prev: dict, mark: set):
    """
    Check neighbours using deque.

    for each neighbour of i, j if a new path is found update the parameters
    (weight, weight_heap, prev, mark)
    """
    len_l = len(grid)
    len_c = len(grid[0])
    dep = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
           (1, 1)]
    for v, h in dep:
        ni, nj = i + v, j + h  # neighbour (ni, nj)
        if 0 <= ni < len_l and 0 <= nj < len_c and (ni, nj) not in mark:
            curr_weight = weight[i, j] + cost(grid, i, j, ni, nj)
            w = weight[ni, nj]
            if curr_weight < w:
                weight_dq.remove((w, (ni, nj)))
                bisect.insort(weight_dq, (curr_weight, (ni, nj)))
                weight[ni, nj] = curr_weight
                prev[ni, nj] = (i, j)
    return


def init_all_vertex(grid, weight: dict, weight_heap: list,
                    start: tuple):
    """Initialition of all vertex weight to +infinity except start vertex."""
    len_l = len(grid)
    len_c = len(grid[0])
    for i in range(len_l):
        for j in range(len_c):
            heapq.heappush(weight_heap, (inf, (i,j)))
            weight[(i, j)] = inf
    weight[start] = 0
    heapq.heappush(weight_heap, (0, start))
    return


def init_all_vertex_sd(grid, weight: dict,
                       sorted_weight: SortedDict, start: tuple):
    """Initialition of all vertex weight to +infinity except start vertex."""
    len_l = len(grid)
    len_c = len(grid[0])
    sorted_weight[inf] = set()
    for i in range(len_l):
        for j in range(len_c):
            weight[(i, j)] = inf
            sorted_weight[inf].add((i, j))
    sorted_weight[inf].remove(start)
    sorted_weight[0] = set([start,])
    weight[start] = 0
    return


def init_all_vertex_deque(grid, weight: dict, weight_deque: deque,
                          start: tuple):
    """Initialise of all vertex weight to +infinity."""
    len_l = len(grid)
    len_c = len(grid[0])
    for i in range(len_l):
        for j in range(len_c):
            weight_deque.append((inf, (i, j)))
            weight[(i, j)] = inf
    weight_deque.remove((inf, start))
    weight_deque.appendleft((0, start))
    weight[start] = 0
    return


def dijkstra_matrix_heap(grid, start: tuple, target: tuple):
    """Dijkstra algorithm using a heap and graph being a matrix."""
    weight_heap = []
    weight = {}
    mark = set()
    prev = {}
    init_all_vertex(grid, weight, weight_heap, start)
    while True:
        # found the vertex with smallest weight
        w, (curr_i, curr_j) = heapq.heappop(weight_heap)
        if w == inf:
            raise ValueError("No path found")
        if (curr_i, curr_j) == target :
            break
        mark.add((curr_i, curr_j))
        # for each neighbour modify weight dico if a better path is found
        check_neighbours(grid, curr_i, curr_j, weight, weight_heap, prev, mark)
    return get_path(prev, start, target)


def dijkstra_matrix_deque(grid, start: tuple, target: tuple):
    """Dijkstra algorithm using a deque and graph being a matrix."""
    weight_deque = deque()
    weight = {}
    mark = set()
    init_all_vertex_deque(grid, weight, weight_deque, start)
    prev = {}
    while True:
        # found the vertex with smallest weight
        w, (curr_i, curr_j) = weight_deque.popleft()
        if w == inf:
            raise ValueError("No path found")
        if (curr_i, curr_j) == target :
            break
        mark.add((curr_i, curr_j))
        # for each neighbour modify weight dico if a better path is found
        check_neighbours_dq(grid, curr_i, curr_j, weight, weight_deque, prev, mark)
    return get_path(prev, start, target)


def dijkstra_matrix_sorted_dict(grid, start: tuple, target: tuple):
    """Dijkstra algorithm using a sorted dict and graph being a matrix."""
    sorted_weight = SortedDict()
    weight = {}
    prev = {}
    mark = set()
    init_all_vertex_sd(grid, weight, sorted_weight, start)
    while True:
        # get the vertex with smallest weight
        curr_weight, vertex_set = sorted_weight.popitem(index=0)
        (v_i, v_j) = vertex_set.pop()
        if curr_weight == inf:
            raise ValueError("No path found")
        if (v_i, v_j) == target:
            break
        mark.add((v_i, v_j))
        if len(vertex_set) != 0:
            sorted_weight[curr_weight] = vertex_set
        check_neighbours_sd(grid, v_i, v_j, weight, sorted_weight, prev, mark)
    return get_path(prev, start, target)


if __name__ == "__main__" :
    import random as rd
    import time
    N = 500
    M = [[rd.randint(0, 1000) for i in range(N)] for i in range(N)]
    vertex_start = (rd.randint(0, N-1), rd.randint(0, N-1))
    vertex_end = (rd.randint(0, N-1), rd.randint(0, N-1))

    start = time.time()
    m = dijkstra_matrix_heap(M, vertex_start, vertex_end)
    end = time.time()
    print("heap time = ", end-start)

    start = time.time()
    n = dijkstra_matrix_deque(M, vertex_start, vertex_end)
    end = time.time()
    print("deque time = ", end-start)

    start = time.time()
    l = dijkstra_matrix_sorted_dict(M, vertex_start, vertex_end)
    end = time.time()
    print("sorted dict time = ", end-start)
    assert(m == l ==n)
