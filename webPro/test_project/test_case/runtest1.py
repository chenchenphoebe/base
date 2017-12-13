#-*- coding:utf-8 -*-
# from test_case import test_baidu
# from  test_case import test_youdao
import test_baidu
import test_youdao

import unittest

suite = unittest.TestSuite()
suite.addTest(test_baidu.MyTest("test_baidu"))
suite.addTest(test_youdao.MyTest("test_youdao"))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run()


