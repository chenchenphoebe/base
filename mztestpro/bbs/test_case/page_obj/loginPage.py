#-*- coding:utf-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from .base import Page
from time import sleep

class login(Page):
    '''用户登录页面'''
    url = '/'
    #Actions
    # bbs_login_user_loc = (By.XPATH, "//div[@id = 'mzCust']/div[@class='loginArea']")
    # bbs_login_button_loc = (By.XPATH,"//p/a[@id='mzLogin']")

    def bbs_login(self):
        # ActionChains(driver).move_to_element(self.bbs_login_user_loc).perform()
        # self.find_element(*self.bbs_login_user_loc).click()
        # self.find_element(*self.bbs_login_button_loc).click()
        pass
    # login_username_loc = (By.ID,"account")
    # login_password_loc = (By.ID,"password")
    # login_button_loc = (By.ID,"login")
    login_username_loc = (By.XPATH,"//div[@class='cycode-selectbox']/input[@id='account']")
    login_password_loc = (By.XPATH,"//div[@class='normalInput fieldInput']/input[@id='password']")
    login_button_loc = (By.XPATH,"//a[@id='login']")
    #-------------!在self.find_element(self.login_username_loc)中传入参数，在*loc中当做一个参数，无法获取到---------
    #登录用户名
    def login_username(self,username):
        print('start to send val')
        # self.find_element(*self.login_username_loc).clear()
        #self.find_element(*self.login_username_loc).send_keys(username)
        self.find_element(By.XPATH,"//div[@class='cycode-selectbox']/input[@id='account']").send_keys(username)

    def login_password(self,password):
        self.find_element(By.XPATH,"//div[@class='normalInput fieldInput']/input[@id='password']").send_keys(password)

    def login_button(self):
        self.find_element(By.XPATH,"//a[@id='login']").click()

    def user_login(self,username = 'username',password = "123456"):
        self.open1()
        # self.bbs_login()
        print("input uasername password")
        self.login_username(username)
        self.login_password(password)
        self.login_button()
        sleep(1)

    user_error_hint_loc = (By.XPATH,"//span[@for='account']")
    pawd_error_hint_loc = (By.XPATH,"//span[@for='password']")
    user_login_success_loc = (By.ID,"mzCustName")

    #用户名错误提示
    def user_error_hint(self):
        return self.find_element(By.XPATH,"//span[@class='tip-font']").text

    def pawd_error_hint(self):
        return self.find_element(By.XPATH,"//span[@class='tip-font']").text

    def user_login_success(self):
        return self.find_element(By.XPATH,"//label[@for='remember']").text


