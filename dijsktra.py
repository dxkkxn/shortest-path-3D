import math
import heapq
from collections import deque
from sortedcontainers import SortedDict

def cost(grid, v1i, v1j, v2i, v2j):
    """
        cost to go from v1 vertex to v2 vertex
    """
    #we detect a diagonal mouvement
    if abs(v1i-v2i) and abs(v1j-v2j) :
        weight = math.sqrt(2) * abs((grid[v1i][v1j] + grid[v2i][v2j])/2)
    else:
        weight = abs((grid[v1i][v1j] + grid[v2i][v2j])/2)
    return weight


def check_neighbours_sd(grid, i, j, weight, sorted_weight, prev, mark):
    len_l = len(grid)
    len_c = len(grid[0])
    dep = [-1, 0, 1]
    for v in dep:
        for h in dep:
            ni, nj = i+v, j+h #neighbour (ni, nj)
            if not(v == 0 and h == 0) and  0 <= ni < len_l \
               and 0 <=nj < len_c and (ni, nj) not in mark:
                curr_weight = weight[(i, j)] + cost(grid, i, j, ni, nj)
                if curr_weight < weight[(ni, nj)]:
                    weight[(ni, nj)] = curr_weight
                    sorted_weight[(ni, nj)] = curr_weight
                    prev[(ni, nj)] = (i, j)
    return

def check_neighbours(grid, i, j, weight, weight_heap, prev, mark):
    len_l = len(grid)
    len_c = len(grid[0])
    dep = [-1, 0, 1]
    for v in dep:
        for h in dep:
            ni, nj = i+v, j+h #neighbour (ni, nj)
            if not(v == 0 and h == 0) and  0 <= ni < len_l and 0 <= nj < len_c \
               and (ni, nj) not in mark:
                curr_weight = weight[(i, j)] + cost(grid, i, j, ni, nj)
                if curr_weight < weight[(ni, nj)]:
                    heapq.heappush(weight_heap, ((ni, nj), curr_weight))
                    weight[(ni, nj)] = curr_weight
                    prev[(ni, nj)] = (i, j)
    return

def check_neighbours_dq(grid, i, j, weight, weight_dq, prev, mark):
    len_l = len(grid)
    len_c = len(grid[0])
    dep = [-1, 0, 1]
    for v in dep:
        for h in dep:
            ni, nj = i+v, j+h #neighbour (ni, nj)
            if not(v == 0 and h == 0) and  0 <= ni < len_l and 0 <= nj < len_c \
               and (ni, nj) not in mark:
                curr_weight = weight[(i, j)] + cost(grid, i, j, ni, nj)
                w = weight[(ni, nj)]
                if curr_weight < w:
                    weight_dq.remove(((ni, nj), w))
                    index = i_deque(weight_dq, curr_weight)
                    weight_dq.insert(index, ((ni, nj), curr_weight))
                    weight[(ni, nj)] = curr_weight
                    prev[(ni, nj)] = (i, j)
    return


def init_all_vertex(grid, weight, weight_heap):
    """
    Initialiation of all vertex weight to +infinity
    """
    len_l = len(grid)
    len_c = len(grid[0])
    for i in range(len_l):
        for j in range(len_c):
            heapq.heappush(weight_heap, ((i,j), float('inf')))
            weight[(i, j)] = float('inf')
    return

def init_all_vertex_sd(grid, weight, sorted_weight):
    """
    Initialiation of all vertex weight to +infinity
    """
    len_l = len(grid)
    len_c = len(grid[0])
    for i in range(len_l):
        for j in range(len_c):
            weight[(i, j)] = float('inf')
            sorted_weight[(i, j)] = float('inf')
    return

def init_all_vertex_deque(grid, weight, weight_deque):
    """
    Initialiation of all vertex weight to +infinity
    """
    len_l = len(grid)
    len_c = len(grid[0])
    for i in range(len_l):
        for j in range(len_c):
            weight_deque.append(((i,j), float('inf')))
            weight[(i, j)] = float('inf')
    return


def i_deque(weight_deque, val):
    res = len(weight_deque)
    for i in range(len(weight_deque)):
        if weight_deque[i][1] > val :
            res = i
            break
    return res

def get_path(grid, prev, start, target):
    curr_node= target
    path = [target]
    while curr_node != start:
        path.append(prev[curr_node])
        curr_node = prev[curr_node]
    path.reverse()
    return path


def dijkstra(grid, start : tuple, target: tuple):
    weight_heap = []
    weight = {}
    mark = set()
    init_all_vertex(grid, weight, weight_heap)
    weight[start] = 0
    heapq.heappush(weight_heap, (start, 0))
    prev = {}
    while True:
        # found the vertex with smallest weight
        (curr_i, curr_j), w = heapq.heappop(weight_heap)
        if (curr_i, curr_j) == target :
            break;
        mark.add((curr_i, curr_j))
        # for each neighbour modify weight dico if a better path is found
        check_neighbours(grid, curr_i, curr_j, weight, weight_heap, prev, mark)
    return get_path(grid, prev, start, target)

def dijkstra_deque(grid, start : tuple, target: tuple):
    weight_deque = deque()
    weight = {}
    mark = set()
    init_all_vertex_deque(grid, weight, weight_deque)
    weight_deque.popleft()
    weight_deque.appendleft((start, 0))
    weight[start] = 0
    prev = {}
    while True:
        # found the vertex with smallest weight
        (curr_i, curr_j), w = weight_deque.popleft()
        # print(curr_i, curr_j)
        if (curr_i, curr_j) == target :
            break;
        mark.add((curr_i, curr_j))
        # for each neighbour modify weight dico if a better path is found
        check_neighbours_dq(grid, curr_i, curr_j, weight, weight_deque, prev, mark)
    return get_path(grid, prev, start, target)

def dijkstra_sd(grid, start : tuple, target: tuple):
    sorted_weight = SortedDict()
    weight = {}
    mark = set()
    init_all_vertex_sd(grid, weight, sorted_weight)
    sorted_weight[start] = 0
    weight[start] = 0
    prev = {}
    i = 0
    while True:
        # found the vertex with smallest weight
        (curr_i, curr_j), w = sorted_weight.peekitem(index=i)
        if (curr_i, curr_j) == target :
            break
        mark.add((curr_i, curr_j))
        # for each neighbour modify weight dico if a better path is found
        check_neighbours_sd(grid, curr_i, curr_j, weight, sorted_weight, prev,
                            mark)
        i += 1
    return get_path(grid, prev, start, target)


if __name__ == "__main__" :
    import random as rd
    import time
    N = 500
    M = [[rd.randint(0, 1000) for i in range(N)] for i in range(N)]
    start = time.time()
    m = dijkstra(M, (0, 0), (N-1, N-1))
    end = time.time()

    print("heap time = ", end-start)
    # start = time.time()
    # n = dijkstra_deque(M, (0, 0), (N-1, N-1))
    # end = time.time()
    # print("dq time = ", end-start)
    start = time.time()
    l = dijkstra_sd(M, (0, 0), (N-1, N-1))
    end = time.time()
    print("sq time = ", end-start)
    assert(m==l)
