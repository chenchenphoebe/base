#-*- coding:utf-8 -*-
import unittest
class Test(unittest.TestCase):
    # def setUp(self):
    #     print("test start .....")
    #
    # def tearDown(self):
    #     print("test end ......")

    def setUp(self):
        self.number=raw_input('Enter a number:')
        self.number=int(self.number)

    def test_case1(self):
        print self.number
        self.assertEqual(self.number, 10, msg='Your input is not 10')

    def test_case2(self):
        print self.number
        self.assertEqual(self.number, 20, msg='Your input is not 20')

    @unittest.skip('暂时跳过用例3的测试')
    def test_case3(self):
        print self.number
        self.assertEqual(self.number, 30, msg='Your input is not 30')
    def tearDown(self):
        print 'Test over'

if __name__=='__main__':
    #1:按命名顺序执行测试test case
    # unittest.main()
    #
    # #2:按照加入到suite的顺序执行test case
    # suite = unittest.TestSuite()
    # suite.addTest(Test('test_case2'))
    # suite.addTest(Test('test_case1'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    #3：按照命名顺序执行test case
    test_dir = './'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*.py')
    runner = unittest.TextTestRunner()
    runner.run(discover)
