# -*- coding: utf-8 -*-

__author__ = 'hanbei'
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from Base_Page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class Login_tcloud(BasePage):
    # 定位器
    username_loc = (By.ID, "username")
    password_loc = (By.ID, "password")
    site_loc = (By.NAME, "site")
    domin_user_loc = (By.XPATH, "/html/body/div[2]/div[2]/div/a[2]/span[2]")

    #   打开页面
    def open(self):
        self._open(self.url, self.title)

    #   输入用户名
    def input_username(self, username):
        self.find_element(*self.username_loc).send_keys(username)

    #   输入密码
    def input_password(self, password):
        self.find_element(*self.password_loc).send_keys(password)

    #选择site
    def choose_site(self):
        try:
            #WebDriver提供了Select类来处理下拉框,
            Select(self.find_element(*self.site_loc)).select_by_visible_text(u"深圳-SCD")
        except:
            print "select error"
    # 调用send_keys对象，选择域账户登录
    def click_login(self):
        self.find_element(*self.domin_user_loc).click()
