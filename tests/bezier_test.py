#!/usr/bin/env python3
import sys
sys.path.append('../')
from linear_algebra import Point
from bezier import horner,cubic_bezier
import unittest


class test_bezier(unittest.TestCase):

    def test_horner_value(self):
        self.assertEqual(horner([1,1,1],2), 7)


    def test_value_eq_bezier(self):
        x=Point(1,1,1)
        l_x=[x,x,x]
        with self.assertRaises(ValueError):
            cubic_bezier(l_x)


    def test_value_err_bezier(self):
        x=Point(1,1,1)
        l_x=[x,x,x,x,x]
        with self.assertRaises(ValueError):
            cubic_bezier(l_x)


    def test_att_err_bezier(self):
        x="Mot"
        y="Mot2"
        z="Motus"
        l_x=[x,y,z]
        with self.assertRaises(AttributeError):
            cubic_bezier(l_x)


if __name__ == '__main__':
    unittest.main()
