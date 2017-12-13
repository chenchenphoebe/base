#-*- coding:utf-8 -*-
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
driver.get_screenshot_as_file("baidu.png")
driver.quit()