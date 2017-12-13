#-*- coding:utf-8 -*-
from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("http://www.maiziedu.com")
driver.find_element_by_link_text('登录').click()
time.sleep(5)
# driver.find_element_by_id('id_account_1').send_keys('maizi_test@139.com')
# driver.find_element_by_id('id_passworld_1').send_keys('abc123456')
# driver.find_element_by_id('login_btn').click()
driver.find_element_by_name('account_l').clear()
driver.find_element_by_name('account_l').send_keys('maizi_test@139.com')
print('name')
driver.find_element_by_name('password_l').send_keys('abc123456')
print('password')
driver.find_element_by_xpath("//div[@class='login-box marginB10']/button[@id='login_btn']").click()
driver.find_element_by_xpath("//span[@class='nick_name']/a[@class='sign_out']").click()
print("退出")
driver.implicitly_wait(10)
driver.quit()
