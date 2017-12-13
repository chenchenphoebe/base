#-*- coding:utf-8 -*-
from selenium import webdriver
import time

search_text = ['php','python''ruby']

for text in search_text:
    driver = webdriver.Firefox()
    driver.get("http://www.baidu.com")
    driver.find_element_by_id("kw").send_keys(text)
    driver.find_element_by_id("su").click()

    driver.quit()