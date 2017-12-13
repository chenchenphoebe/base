#-*- coding:utf-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
class Page(object):
    '''页面基础类，用于所有类的继承'''

    base_url = "http://bbs.meizu.com"
    def __init__(self,selenium_driver,base_url=base_url,parent= None):
        self.base_url = base_url
        self.driver = selenium_driver
        self.timeout = 30
        self.parent = parent

    def _open(self,url):
        url = self.base_url + url
        self.driver.get(url)
        right = self.driver.find_element_by_xpath("//div[@id = 'mzCust']/div[@class='loginArea']")
        ActionChains(self.driver).move_to_element(right).perform()
        self.driver.find_element_by_xpath("//p/a[@id='mzLogin']").click()
        # time.sleep(10)
        # self.driver.switch_to.frame('main-form')
        print("_open run end")
        # assert self.on_page(),'Did not land on %s'%url

    def find_element(self,*loc):
        # eleid = self.driver.find_element(By.XPATH,"//div[@class='cycode-selectbox']/input[@id='account']")
        # loc = (By.XPATH,"//div[@class='cycode-selectbox']/input[@id='account']")
        # eleid = self.driver.find_element(loc)
        # print(eleid)
        # return eleid
        # print(loc)
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # -------------!在self.find_element(self.login_username_loc)中传入参数，在*loc中当做一个参数，无法获取到---------
            #---------------*loc的值为((By.XPATH,"//div[@class='cycode-selectbox']/input[@id='account']"),)--------
            #-----------------find_element(val1,val2),需要两个参数，以上是传值错误------------
            return self.driver.find_element(*loc)
        except:
            print u"%s 页面中未能找到 %s 元素" % (self, loc)


    def find_elements(self,*loc):
        return self.driver.find_elements(*loc)

    def open(self):
        self._open(self.url)

    def on_page(self):
        return self.driver.current_url == (self.base_url+self.url)

    def script(self,src):
        return self.driver.execute_script(src)

