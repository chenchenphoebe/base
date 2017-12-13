#-*- coding:utf-8 -*-
from selenium import webdriver
from public import Login

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("http://www.126.com")

Login().user_login(driver)
print(driver.title)
Login().user_logout(driver)