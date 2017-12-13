#-*- coding:utf-8 -*-
from calculator import Count
import unittest

class TestSub(unittest.TestCase):

    def setUp(self):
        print("test case start-----")

    def tearDown(self):
        print("test case end-----")

    def test_sub(self):
        j = Count(2, 3)
        self.assertEqual(j.sub(), -1)

    def test_sub2(self):
        j = Count(76, 41)
        self.assertEqual(j.sub(), 25)


if __name__ == "__main__":
    unittest.main()

