# -*- coding:utf-8 -*-
from test_case import test_baidu
from  test_case import test_youdao
import time
from HTMLTestRunner import HTMLTestRunner
import unittest

# suite = unittest.TestSuite()
# suite.addTest(test_baidu.MyTest("test_baidu"))
# suite.addTest(test_youdao.MyTest("test_youdao"))


if __name__ == "__main__":
    test_dir = "./test_case"
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test_*.py")
    now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    fp = open(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\test_project\report\result%s.html'%now, "wb")
    runner = HTMLTestRunner(stream=fp,title="测试报告",description="用例执行情况")
    runner.run(discover)
    fp.close()




