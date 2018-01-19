#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from pip._vendor.distlib.locators import Page
from selenium.webdriver.support.ui import Select  # 导入下拉框函数
import unittest


class Page(object):
    login_url = 'http://qf-uatqapp-w2/ProductApplication/Application'

    def __init__(self, selenium_driver, base_url=login_url):
        self.base_url = base_url
        self.driver = selenium_driver
        self.timeout = 30
        self.driver.maximize_window()

    def on_page(self):
        return self.driver.current_url == (self.base_url + self.url)

    def _open(self, url):
        url = self.base_url
        self.driver.get(url)
        self.driver.maximize_window()
        # assert self.on_page(), 'Did not land on %s' %url

    def open(self):
        self._open(self.url)

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def switch_frame(self, loc):
        return self.driver.switch_to_frame()


class LoginPage(Page):
    url = '/'
    username_loc = (By.ID, "Account")
    password_loc = (By.ID, "Pwd")
    submit_loc = (By.ID, "Log_Submit")

    def type_username(self, username):
        self.find_element(*self.username_loc).send_keys(username)

    def type_password(self, password):
        self.find_element(*self.password_loc).send_keys(password)

    def submit(self):
        self.find_element(*self.submit_loc).click()


class ProductPage(Page):
    customername_loc = (By.ID, "customerName")
    customerID_loc = (By.ID, "customerIDCard")
    applyCity_loc = (By.ID, "applyCity")

    # productCode_loc = (By.ID,"//option[@value='productCodesyd-6-24']")
    # productCode_value = (By.XPATH,"//option[@value='BYQSF0000']")
    # platform_loc = (By.ID,"platform")
    # platform_value = (By.XPATH,"//option[@value='BYQSF0000']")

    def type_customername(self, customername):
        self.find_element(*self.customername_loc).send_keys(customername)

    def type_customerID(self, customerId):
        self.find_element(*self.customerID_loc).send_keys(customerId)

    def type_applyCity(self, applyCityvalue):
        Select(self.find_element(*self.applyCity_loc)).select_by_value(applyCityvalue)  # 下拉框函数


def test_user_login(driver, username, password):
    page = LoginPage(driver)
    page.open()
    page.type_username(username)
    page.type_password(password)
    page.submit()


def test_apply_product(driver, customername, customerID, applyCityvalue):
    page1 = ProductPage(driver)
    page1.type_customername(customername)
    page1.type_customerID(customerID)
    page1.type_applyCity(applyCityvalue)


def main():
    driver = webdriver.Chrome()
    username = 'jiahua'
    password = 'Quarkhj05'
    customername = u'huajia'
    customerId = '310104198408020057'
    applyCityvalue = '025,025'
    test_user_login(driver, username, password)
    driver.implicitly_wait(30)
    test_apply_product(driver, customername, customerId, applyCityvalue)


if __name__ == '__main__':
    main()
    unittest.main()