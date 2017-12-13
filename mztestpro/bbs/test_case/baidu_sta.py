# -*- coding:utf-8 -*-
# encoding=utf8
# encoding=utf8
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from selenium import webdriver
import unittest
from HTMLTestRunner import HTMLTestRunner
import time
import sys
sys.path.append('./models')
from models.myunit import MyTest

# class MyTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.base_url = "http://www.baidu.com"
#         self.driver.implicitly_wait(10)
#         self.driver.maximize_window()
#
#     def tearDown(self):
#         self.driver.quit()

class Baidu(MyTest):
# class Baidu(unittest.TestCase):
    '''百度搜索测试'''

    # def setUp(self):
    #     self.driver = webdriver.Firefox()
    #     self.driver.implicitly_wait(10)
    #     self.base_url= "http://www.baidu.com"
    #
    # def tearDown(self):
    #     self.driver.quit()

    def test_baidu_search(self):
        #doc string注释用于函数、类和方法，可以通过help()来查看的注释
        '''   搜索关键字：HTMLTestRunner  '''

        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("kw").send_keys("HTMLTestRunner")
        driver.find_element_by_id("su").click()

# if __name__ == '__main__':
#修改当前执行模块为testbaidu，否则无法生成报告
if __name__ == "__main__":
    # testunit = unittest.TestSuite()
    # testunit.addTest(Baidu("test_baidu_search"))
    # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # print(now)
    # fp = file("result" + now + ".html", 'wb')
    # #定义报告保存路径
    # # fp = file('./testresult.html',"wb")
    # runner = HTMLTestRunner(stream=fp, title="百度搜索报告", description="用例执行情况：")
    # runner.run(testunit)
    # fp.close()
    unittest.main()
