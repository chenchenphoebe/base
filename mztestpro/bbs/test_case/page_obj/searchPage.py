#-*- coding:utf-8 -*-
'''
分析：
1.需要输入在文本框中输入值
2.需要点击search按钮
3.跳入到下一个页面，统计是否查询出条数
4.统计是否查询为空
'''
#实际完成：无法定位问题

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from .base import Page
# choose_all_module_loc = (By.XPATH, "//*[@id='myModal']/div/div/div[2]/div/div/table/thead/tr/th[1]/input")
class serachPage(Page):
    url = '/'
    '''页面搜索界面'''
    input_loc = (By.XPATH, "//div[@class='scbar_wrap']/input[@name='srchtxt']")
    button_loc = (By.XPATH, "//div[@class='scbar_wrap']/button[@name='searchsubmit']")
    # table_loc = (By.XPATH, "//div[@id='wp']/div[@class='cl w']/div[@class='mw']/div[@class='tl']/div[@class='mainbox threadlist']/div[@class='tsearch']/table[@class='tsearch']/thread/tr")
    table_loc= (By.XPATH, "//body[@id='nv_search']/div[@id='wp']/div[@class='cl w']")
    idea_loc = (By.XPATH, "(//a[contains(text(),'综合讨论')])[4]")

    # def get_ele_times(self,driver, times, func):
    #     return WebDriverWait(driver, times).until(func)

    def send_val(self, word):
        self.driver.find_element(*self.input_loc).send_keys(word)

    def send_button(self):
        self.driver.find_element(*self.button_loc).click()

    def count_idea(self):
        try:
            # self.get_ele_times(self.driver, 10, self.driver.find_element(*self.table_loc))
            return self.driver.title
        except Exception,  e:
            raise e

    def search_idea(self, word=''):
        self.open2()
        self.send_val(word)
        self.send_button()










