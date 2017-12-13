#-*- coding:utf-8 -*-
import unittest

class Mytest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    @unittest.skip(u"直接跳过测试")
    def test_skip(self):
        print("test skip")

    @unittest.skipIf(3>2,u"当条件为ture时跳过")
    def test_skip_if(self):
        print("test skip if")

    @unittest.skipUnless(3>2,u"当条件为ture时执行测试")
    def test_skip_unless(self):
        print("test skip unless")

    @unittest.expectedFailure
    def test_expected_failure(self):
        self.assertEqual(2,3)

if __name__ == "__main__":
    unittest.main()