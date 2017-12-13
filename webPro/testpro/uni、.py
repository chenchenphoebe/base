#-*- coding:utf-8 -*-
from calculator import Count
import unittest

'创建MyTest()类的好处显而易见，对于测试类和测试方法来说，应将注意力放在具体的用例编写上，'
'无须关心setUp()和tearDown()所做的事情。前提是setUp()和tearDown()所做的事情是每个用例都需要的'


class MyTest(unittest.TestCase):
    def setUp(self):
        print("test case start")

    def tearDown(self):
        print("test case end")


class TestAdd(MyTest):
    # def setUp(self):
    #     print("test add start")
    def test_add(self):
        j = Count(2, 3)
        self.assertEqual(j.add(), 5)


    def test_add2(self):
        j = Count(41, 76)
        self.assertEqual(j.add(), 117)
        # def tearDown(self):
        #     print("test add end")


class TestSub(MyTest):
    # def setUp(self):
    #     print("test sub start")
    def test_sub(self):
        j = Count(2, 3)
        self.assertEqual(j.sub(), -1)

    def test_sub2(self):
        j = Count(71, 46)
        self.assertEqual(j.sub(), 25)
        # def tearDown(self):
        #    print("test sub end")


if __name__ == '__main__':
    # 构造测试集
    # suite=unittest.TestSuite()
    # suite.addTest(TestAdd("test_add"))
    # suite.addTest(TestAdd("test_add2"))
    # suite.addTest(TestSub("test_sub"))
    # suite.addTest(TestSub("test_sub2"))
    # 运行测试集合
    # runner =unittest.TextTestRunner()
    # runner.run(suite)
    unittest.main()