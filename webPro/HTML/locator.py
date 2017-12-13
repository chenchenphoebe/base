#-*- coding:utf-8 -*-
from selenium import webdriver
def find_Telement(*loc):
    driver = webdriver.Firefox()
    driver.get("http://www.baidu.com")
    # eleid = self.driver.find_element(By.XPATH, "//div[@class='cycode-selectbox']/input[@id='account']")
    # loc = (By.XPATH, "//div[@class='cycode-selectbox']/input[@id='account']")
    eleid = driver.find_element(*loc)
    print(type(eleid))
    return eleid
    driver.quit()