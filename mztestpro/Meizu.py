# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Meizu(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_meizu(self):
        driver = self.driver
        driver.get("https://bbs.meizu.cn/search.php?mod=forum&searchid=1&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=android")
        driver.find_element_by_id("scbar_txt").click()
        driver.find_element_by_id("scbar_btn").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | win_ser_1 | ]]
        driver.find_element_by_link_text("Android").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | win_ser_2 | ]]
        driver.get("https://bbs.meizu.cn/viewthread.php?tid=5961017&highlight=")
        driver.find_element_by_id("scbar_txt").click()
        driver.find_element_by_id("scbar_txt").clear()
        driver.find_element_by_id("scbar_txt").send_keys("selenium")
        driver.find_element_by_id("scbar_btn").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | win_ser_3 | ]]
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tbody/tr/th").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tbody/tr/th").click()
        # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | //div[@id='wp']/div/div/div/div/table/tbody/tr/th | ]]
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tbody/tr/th").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tbody/tr/th").click()
        # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | //div[@id='wp']/div/div/div/div/table/tbody/tr/th | ]]
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tbody/tr/th").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tbody/tr/th").click()
        # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | //div[@id='wp']/div/div/div/div/table/tbody/tr/th | ]]
        driver.get("https://bbs.")

        driver.close()

        driver.close()

        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tb").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tb").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/table/tb").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/di").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/di").click()
        driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/di").click()
        driver.close()

    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
