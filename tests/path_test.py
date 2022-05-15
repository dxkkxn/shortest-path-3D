from sortedcontainers import sorteddict
import sys
sys.path.append('../')
from linear_algebra import Point
import dijkstra
import a_star
import unittest
import heapq
from collections import deque

class test_dijkstra(unittest.TestCase):

    def test_dijkstra_sorted_dict(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        start,target=(0,2),(3,0)
        path=dijkstra.dijkstra_matrix_sorted_dict(M,start,target)
        self.assertEqual(path, [(0, 2), (1, 2), (2, 1), (3, 0)])

    def test_dijkstra_heap(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        start,target=(0,2),(3,0)
        path=dijkstra.dijkstra_matrix_heap(M,start,target)
        self.assertEqual(path, [(0, 2), (1, 2), (2, 1), (3, 0)])

    def test_dijkstra_deque(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        start,target=(0,2),(3,0)
        path=dijkstra.dijkstra_matrix_deque(M,start,target)
        self.assertEqual(path, [(0, 2), (1, 2), (2, 1), (3, 0)])

    def test_a_star(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        start,target=(0,2),(3,0)
        path=a_star.a_star_matrix_sorted_dict(M,start,target)
        self.assertEqual(path, [(0, 2), (1, 2), (2, 1), (3, 0)])


    def test_start_in_init_deque(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        weight=deque()
        dijkstra.init_all_vertex_deque(M, {}, weight, (0,0))
        self.assertIn((0,(0,0)), weight)

    def test_start_in_init_sd(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        weight=sorteddict.SortedDict()
        dijkstra.init_all_vertex_sd(M, {}, weight, (0,0))
        self.assertEqual(weight[0],{(0, 0)})

    def test_dist(self):
        self.assertEqual(a_star.euclidian_distance((0,0),(1,1)),2**0.5)

    def test_start_in_init_heap(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        weight=[]
        dijkstra.init_all_vertex(M, {}, weight, (0,0))
        self.assertIn((0,(0,0)), weight)

    def test_cost(self):
        M=[[100,100,1],
           [100,1,1],
           [100,1,100],
           [1,1,100]]
        weight=[]
        cost=dijkstra.cost(M,0,0,1,1)
        self.assertAlmostEqual(round(cost),71)

    def test_cost_a(self):
        M=[[2,2,1],
           [2,1,1],
           [2,1,2],
           [1,1,2]]
        weight=[]
        cost=a_star.cost_a(M,0,0,1,1,(3,2))
        self.assertAlmostEqual(round(cost),2)

if __name__ == '__main__':
    unittest.main()
