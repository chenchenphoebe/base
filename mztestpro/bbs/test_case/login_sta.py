#-*- coding:utf-8 -*-
from time import sleep
import unittest,random,sys
sys.path.append(".\models")
sys.path.append(".\page_obj")
from models import myunit,function,driver
from page_obj.loginPage import login
from models.log import log

# class loginTest(unittest.TestCase):
class loginTest(myunit.MyTest):
    logger = log()
    '''社区登录测试'''
    #测试用户登录
# class loginTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = driver.browser()
#         self.driver.implicitly_wait(10)
#         self.driver.maximize_window()
#         self.logger = log()
#
#     def tearDown(self):
#         self.driver.quit()

    def user_login_verify(self,username="",password=""):
        login(self.driver).user_login(username,password)

    def test_login1(self):
        '''用户名密码为空'''
        try:
            self.user_login_verify()#用户登录操作，调用loginpage页面的login
            po = login(self.driver)
            self.assertEqual(po.user_error_hint(),u"请填写完整的登录信息")
            self.assertEqual(po.pawd_error_hint(),u"请填写完整的登录信息")
            # self.logger.error(u"请填写完整的登录信息")
            function.insert_img(self.driver,"user_pawd_empty.jpg")
        except Exception:
            self.logger.error(u"请填写完整的登录信息")

    def test_login2(self):
        '''用户名正确密码为空'''
        try:
            self.user_login_verify(username="pytest")
            po = login(self.driver)
            self.assertEqual(po.pawd_error_hint(), u"请填写完整的登录信息")
            # self.logger.info(u"请填写完整的登录信息")
            function.insert_img(self.driver, "pawd_empty.jpg")
        except Exception :
            self.logger.info(u"请填写完整的登录信息")

    def test_login3(self):
        '''用户名为空密码正确'''
        try:
            self.user_login_verify(password="abc123456")
            po = login(self.driver)
            self.assertEqual(po.user_error_hint(),u"请填写完整的登录信息")
            # self.logger.warning(u"请填写完整的登录信息")
            function.insert_img(self.driver,"user_empty.jpg")
        except Exception:
            self.logger.info(u"请填写完整的登录信息")

    def test_login4(self):
        '''用户名与密码不匹配'''
        try:
            character = random.choice("zxxbcncmakjsjajdddkw")
            username = "zhangsan"+character
            self.user_login_verify(username=username,password="123456")
            po = login(self.driver)
            self.assertEqual(po.pawd_error_hint(),u"请点击按钮进行验证")
            # self.logger.error(u"请填写完整的登录信息")
            function.insert_img(self.driver,"user_pawd_error.jpg")
        except Exception:
            self.logger.error(u"请填写完整的登录信息")

    def test_login5(self):
        '''用户名密码正确'''
        try:
            self.user_login_verify(username="zhangsan",password="123456")
            sleep(2)
            po = login(self.driver)
            self.assertEqual(po.user_login_success(),"记住登录状态")
            # self.logger.error(u"请填写完整的登录信息")
            function.insert_img(self.driver,"user_pawd_ture.jpg")
        except Exception:
            self.logger.error(u"请填写完整的登录信息")

if __name__ == "__main__":
    # unittest.main()

    suite = unittest.TestSuite()
    suite.addTest(loginTest('test_login1'))
    suite.addTest(loginTest('test_login2'))
    # suite.addTests((loginTest,{"test_login1","test_login2","test_login3","test_login4","test_login5"}))
    runner = unittest.TextTestRunner()
    runner.run(suite)