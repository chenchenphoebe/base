# -*- coding: utf-8 -*-

__author__ = 'hanbei'
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from unittest.case import _AssertRaisesContext

from getconfigs import GetConfigs
from Base_Page import BasePage

cfg = GetConfigs()
scripts_address = cfg.getstr("TestScripts", 'scripts_address', "common")
module_address = cfg.getstr("TestScripts", 'module_address', "common")
test_project = cfg.getstr("TestProject", "test_project", "common")


class Create_Scripts(BasePage):
    # 定位器
    manage_scripts_loc = (By.CSS_SELECTOR, "#toTestCaseBtn>span.lang")
    scripts_num_loc = (By.CSS_SELECTOR, "#dTable_length>label>select")
    table_loc = (By.ID, "dTable")
    tbody_loc = (By.TAG_NAME, "tbody")
    rows_loc = (By.TAG_NAME, "tr")
    coll_loc = (By.TAG_NAME, "td")
    all_scripts_loc = (By.CSS_SELECTOR, "#dTable>thead>tr>th.choose.sorting_disabled>input")
    delete1_loc = (By.CSS_SELECTOR, "#searchDiv>div.searchArea>table>tbody>tr>td:nth-child(7)>div>button.btn.btn-sm.btn-warning.dropdown-toggle")
    delete2_loc = (By.CSS_SELECTOR, "#deleteMore>span")
    confirm_loc = (By.LINK_TEXT, u"确定")
    add_loc = (By.ID, "addBtn")
    input_name_loc = (By.NAME, "caseName")
    file_type_loc = (By.ID, "testType")
    scripts_path_loc = (By.NAME, "casePath")
    common_path_loc = (By.NAME, "commonPath")
    save_icon_loc = (By.CSS_SELECTOR, "span.glyphicon.glyphicon-ok")
    exists_one_scripts_loc = (By.CSS_SELECTOR, "#tableBody>tr:nth-child(1)>td:nth-child(8)>a.btn.btn-sm.btn-danger>span.lang")
    module1_loc = (By.LINK_TEXT, u"模块管理")
    module2_loc = (By.XPATH, "/html/body/div[1]/aside[1]/section/ul/li[3]/ul/li[1]/a/span")
    delete_module_loc = (By.XPATH, "//*[@id='tableBody']/tr[1]/td[5]/a[2]")
    exists_one_mudule_loc = (By.CSS_SELECTOR, "# tableBody > tr > td:nth-child(5) > a.btn.btn-sm.btn-danger > span.lang")
    mudule_add_loc = (By.XPATH, "//*[@id='searchDiv']/div[1]/table/tbody/tr/td[3]/div/button")
    SVN_add_loc = (By.LINK_TEXT, u"从Svn根路径新增")
    module_svn_loc = (By.CSS_SELECTOR, "#editForm>div>div.box-body>div:nth-child(4)>div>input")
    module_common_loc = (By.CSS_SELECTOR, "#editForm>div>div.box-body>div:nth-child(5)>div>input")
    save_module_loc = (By.LINK_TEXT, u"保存")


    #点击管理脚本u
    def manage_scripts(self):
        self.find_element(*self.manage_scripts_loc).click()

    #选择每页显示的脚本数
    def scripts_num_display(self):
        var = Select(self.find_element(*self.scripts_num_loc))
        var.select_by_visible_text("25")

    #当前脚本数目
    def current_scripts_sum(self):
        table = self.find_element(*self.table_loc)
        table_body = table.find_element(*self.tbody_loc)
        table_rows = table_body.find_elements(*self.rows_loc)
        return len(table_rows)

    #获取脚本名称
    def get_scripts_name(self, i, type):
        table = self.find_element(*self.table_loc)
        table_body = table.find_element(*self.tbody_loc)
        table_rows = table_body.find_elements(*self.rows_loc)
        if type == "1":
            scripts_name = table_rows[i].find_elements(*self.coll_loc)[1].text
        else:
            scripts_name = table_rows[i].find_elements(*self.coll_loc)[0].text
        return scripts_name

    #全选所有脚本
    def select_all_scripts(self):
        self.find_element(*self.all_scripts_loc).click()

    #批量删除脚本
    def delete_all_scripts(self):
        self.find_element(*self.delete1_loc).click()
        self.find_element(*self.delete2_loc).click()

    #确认删除
    def confirm_delete(self):
        alert = self.driver.switch_to_alert()
        alert.accept()
        self.find_element(*self.confirm_loc).click()

    #新增脚本
    def add_script(self):
        self.find_element(*self.add_loc).click()

    #输入脚本名称
    def input_name(self, name):
        self.find_element(*self.input_name_loc).send_keys(name)

    #选择文件类型
    def choose_file_type(self):
        fileType = Select(self.find_element(*self.file_type_loc))
        fileType.select_by_visible_text("Python Script")

    #输入脚本路径
    def scripts_path(self, scripts_name):
#         self.find_element(*self.scripts_path_loc).send_keys(scripts_address + test_project + "/" + scripts_name)
        self.find_element(*self.scripts_path_loc).send_keys(scripts_address + "/" + scripts_name)

    #输入Common路径
    def common_path(self):
#         self.find_element(*self.common_path_loc).send_keys(scripts_address + test_project + "/" + "common")
        self.find_element(*self.common_path_loc).send_keys(scripts_address + "/" + "common")

    #点击保存脚本按钮
    def save_scripts(self):
        self.find_element(*self.save_icon_loc).click()
        self.find_element(*self.confirm_loc).click()

    #存在一条脚本
    def exists_one_scripts(self):
        if self.find_element(*self.exists_one_scripts_loc):
            return True

    #点击模块管理
    def manage_module(self):
        self.find_element(*self.module1_loc).click()
        self.find_element(*self.module2_loc).click()

    #删除module
    # def delete_module(self, times):
    #     for i in range(times):
    #         print i
    #         self.assertEqual(u"确认删除吗？", self.close_alert_and_get_its_text())
    #         # if self.find_element(self.delete_module_loc):
    #         self.find_element(self.delete_module_loc).click()
    #         # else:
    #         #     self.img_screenshot(u'删除找不到')
    #         #     return False

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    #判断是否存在一个模块
    def exists_one_module(self):
        if self.find_element(*self.exists_one_mudule_loc):
            return True

    #从SVN目录新增
    def add_SVN_module(self):
        self.find_element(*self.mudule_add_loc).click()
        self.find_element(*self.SVN_add_loc).click()

    #输入SVN地址并保存确认
    def module_SVN_address(self):
        self.find_element(*self.module_svn_loc).send_keys(module_address + "/" + "src")
        self.find_element(*self.save_module_loc).click()
        self.find_element(*self.confirm_loc).click()

























