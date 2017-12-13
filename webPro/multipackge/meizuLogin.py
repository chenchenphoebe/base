#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest

class Login_meizu(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://bbs.meizu.cn/'
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        driver = self.driver
        driver.get(self.baseUrl)
        right=driver.find_element_by_xpath("//div[@id = 'mzCust']/div[@class='loginArea']")
        ActionChains(driver).move_to_element(right).perform()
        # driver.find_element_by_link_text('Flyme').click()
        time.sleep(10)
        driver.find_element_by_xpath("//p/a[@id='mzLogin']").click()
        time.sleep(2)
        val = driver.find_element_by_xpath("//div[@class='cycode-selectbox']/input[@id='account']").is_displayed()
        print('play account'+ str(val))
        driver.find_element_by_id('account').send_keys('123')
        driver.find_element_by_id('password').send_keys('123')
        driver.find_element_by_id('login').click()
        time.sleep(10)


if __name__ == "__main__":
    unittest.main()
