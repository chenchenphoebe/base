#-*- coding:utf-8 -*-
import unittest


class ProCert(unittest.TestCase):

    def setUp(self):
        #执行转圈，无法执行
        # self.number = raw_input('Enter a number:')
        # self.number = int(self.number)
        self.number = 20
        self.number = int(self.number)

    @unittest.skip("直接跳过")
    def test_ok(self):
        print self.number
        self.assertEqual(self.number, 10, msg='Your input is not 10')

    def test_case2(self):
        print self.number
        self.assertEqual(self.number, 20, msg='Your input is not 20')

    def tearDown(self):
        pass


if __name__ == "__main__":

    # unittest.main()
    test_dir = './'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*.py')
    runner = unittest.TextTestRunner()
    runner.run(discover)
