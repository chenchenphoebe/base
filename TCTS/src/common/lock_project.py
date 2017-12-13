# -*- coding: utf-8 -*-

__author__ = 'hanbei'
from selenium.webdriver.common.by import By

from getconfigs import GetConfigs
from Base_Page import BasePage

cfg = GetConfigs()
test_project = cfg.getstr("TestProject", "test_project", "common")


class Lock_project(BasePage):
    # 定位器
    lock_item_loc = (By.CSS_SELECTOR, "#navbar-collapse>ul>li>a>span.lang")
    click_lock_project_loc = (By.LINK_TEXT, test_project)
    project_name_loc = (By.CSS_SELECTOR, "#selectedProj")
    #点击项目管理
    def lock(self):
        self.find_element(*self.lock_item_loc).click()

    #点击项目
    def click_project(self):
        self.find_element(*self.click_lock_project_loc).click()

    #获得项目名称
    def get_project_name(self):
        return self.find_element(*self.project_name_loc).text









