# -*- coding: utf-8 -*-

__author__ = 'hanbei'
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from Base_Page import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class Create_project(BasePage):
    # 定位器
    project_manage_loc = (By.LINK_TEXT, u"项目管理")
    increase_button_loc = (By.CSS_SELECTOR, "#addBtn>span.lang")
    test_project_loc = (By.NAME, "projName")
    choose_project_loc = (By.CSS_SELECTOR, "#pidDiv>div>select")
    vpm_loc = (By.NAME, "projVpm")
    vpm_email_loc = (By.NAME,"vpmEmail")
    save_project_loc = (By.CSS_SELECTOR,"#saveBtn>span.lang")
    confirm_loc = (By.LINK_TEXT,u"确定")

    #点击项目管理
    def project_manage(self):
        self.find_element(*self.project_manage_loc).click()

    #   点击新增按钮
    def increase_button(self):
        self.find_element(*self.increase_button_loc).click()

    #输入测试项目
    def input_project(self, project):
        self.find_element(*self.test_project_loc).send_keys(project)

    #选择公司项目
    def choose_project(self):
        project = Select(self.find_element(*self.choose_project_loc))
        project.select_by_visible_text("3G_Smart_Qwerty")

    #输入VPM
    def input_vpm(self, vpm):
        self.find_element(*self.vpm_loc).send_keys(vpm)

    #输入VPM email
    def input_vpmEmail(self, vpmEmail):
        self.find_element(*self.vpm_email_loc).send_keys(vpmEmail)

    #保存创建的项目
    def save_project(self):
        self.find_element(*self.save_project_loc).click()

    #确认创建成功
    def confirm_project(self):
        self.find_element(*self.confirm_loc).click()








