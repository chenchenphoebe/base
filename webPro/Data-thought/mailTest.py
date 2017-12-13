#-*- coding:utf-8 -*-
from selenium import webdriver
from public import Login

class Logintest():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.get("http://www.126.com")

    def test_admin_login(self):
        username = 'admin'
        password = 'admin'
        Login().user_login(self.driver,username,password)
        self.driver.quit()

    def test_guest_login(self):
        username = 'guest'
        password = '123'
        Login().user_login(self.driver, username, password)
        self.driver.quit()

email = Logintest()
email.test_admin_login()
# email.test_guest_login()

