#-*- coding:utf-8 -*-
from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("http://www.126.com")

#login
driver.switch_to.frame('x-URS-iframe')
driver.find_element_by_name("email").clear()
driver.find_element_by_name("email").send_keys("username")
driver.find_element_by_name("password").clear()
driver.find_element_by_name("password").send_keys("password")
driver.find_element_by_id("dologin").click()

#login \write\detele

# driver.find_element_by_xpath(".//*[@id='nextTheme']").click()
# driver.find_element_by_id("nextTheme").click()
time.sleep(3)
driver.quit()