#-*- coding:utf-8 -*-
import unittest
# import pytest

class projCert(unittest.TestCase):


    def setUp(self):
        # cls.number = raw_input('Enter a number:')
        # cls.number = int(cls.number)
        self.number = 10
        self.number = int(self.number)

    def test_ok(self):
        print self.number
        self.assertEqual(self.number, 10, msg='Your input is not 10')

    def test_case2(self):
        print self.number
        self.assertEqual(self.number, 20, msg='Your input is not 20')

    @classmethod
    def tearDownClass(cls):
        pass




if __name__ == "__main__":
    # unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(projCert('test_ok'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    test_dir = './'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*.py')
    runner = unittest.TextTestRunner()
    runner.run(discover)

