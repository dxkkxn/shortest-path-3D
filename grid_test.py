import unittest
import grid

class test_grid(unittest.TestCase):

    def test_grid_size(self):
        g=grid.Grid(5,1)
        self.assertEqual(len(g.grid),5)


    def test_smooth_grid_size(self):
        g=grid.Grid(5,1)
        g.smooth(2)
        self.assertEqual(len(g.grid),5)


    def test_tuckey_grid_size(self):
        g=grid.Grid(5,1)
        g.tuckey_smooth(2)
        self.assertEqual(len(g.grid),5)


    def test_grid_index_error(self):
        g=grid.Grid(5,1)
        with self.assertRaises(IndexError):
            g[7][1]


    def test_grid_type_error(self):
        g=grid.Grid(5,1)
        with self.assertRaises(TypeError):
            g.calculate_sense(("a","b"),("c","d"))


    def test_grid_attr_err(self):
        g=grid.Grid(5,1)
        with self.assertRaises(AttributeError):
            mix=g.color(0,0)
            self.assertEqual(mix,(172,159,138))


    def test_grid_color(self):
        g=grid.Grid(5,1)
        g.tuckey_smooth(2)
        mix=g.color(0,0)
        self.assertEqual(mix,(172,159,138))

if __name__ == '__main__':
    unittest.main()
