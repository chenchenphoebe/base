# -*- coding: utf-8 -*-

__author__ = 'hanbei'
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from globalparameter import test_plan

from getconfigs import GetConfigs
from Base_Page import BasePage
from time import sleep


class Create_task(BasePage):
    # 定位器
    MTBF_plan_loc = (By.XPATH, "//li[4]/ul/li[3]/a/span")
    plan_loc = (By.LINK_TEXT, test_plan)
    task_button_loc = (By.ID, "addTaskBtn")
    add_task_loc = (By.NAME, "groupName")
    pc_name_loc = (By.XPATH, "//*[@id='first']/div[2]/div[1]/select")
#     pc_name_loc = (By.XPATH, "//*[@name='clientId']")
    timeout_loc = (By.NAME, "timeoutMin")
    next_loc = (By.ID, "next")
    device_display_loc = (By.LINK_TEXT, u"···")
    device_tbody_loc = (By.CSS_SELECTOR, "#devices")
    device_row_loc = (By.TAG_NAME, "tr")
    save_device_loc = (By.CSS_SELECTOR, "#saveDeviceBtn>span.lang")
    scripts_loc = (By.ID, "selectCaseBtn")
    add_scripts_loc = (By.CSS_SELECTOR, "#caseListTb>thead>tr>th.choose.sorting_disabled>input")
    save_scripts_loc = (By.CSS_SELECTOR, "#saveCaseListBtn>span.lang")
    add_new1_loc = (By.XPATH, "//*[@id='addTaskTable']/tbody/tr/td[8]/a[2]/span")
    save_task_loc = (By.LINK_TEXT, u"保存")
    confirm_task_loc = (By.LINK_TEXT, u"确定")
    wait_task_loc = (By.CSS_SELECTOR, '#tableBody>tr>td.lang')
    scripts_num_loc = (By.CSS_SELECTOR, "#caseListTb_length>label>select")
    choose_module_loc = (By.LINK_TEXT, u"选择模块")
    choose_all_module_loc = (By.XPATH, "//*[@id='myModal']/div/div/div[2]/div/div/table/thead/tr/th[1]/input")
    save_module_loc = (By.CSS_SELECTOR, "#saveModuleBtn>span.lang")

    # 点击MTBF测试计划
    def click_MTBF_plan(self):
        self.find_element(*self.MTBF_plan_loc).click()

    #判断Plan是否存在
    def plan_exists(self):
        if self.find_element(*self.plan_loc):
            return True
    # 点击plan
    def click_plan(self):
        self.find_element(*self.plan_loc).click()

    #添加测试任务
    def add_task(self, test_task):
        self.find_element(*self.task_button_loc).click()
        self.find_element(*self.add_task_loc).send_keys(test_task)

    #选择测试的PC名称
    def PC_name(self, pc_name):
        var = Select(self.find_element(*self.pc_name_loc))
        var.select_by_visible_text(pc_name)

    #清除设置
    def clear_timeout(self):
        self.find_element(*self.timeout_loc).send_keys("")
        self.find_element(*self.next_loc).click()

    #点击显示设备
    def display_device(self, index):
        if index == 1:
#             self.find_element(*self.device_display_loc).click()
            self.find_element(By.XPATH, ".//*[@id='addTaskTable']/tbody/tr/td[3]/a").click()
        elif index == 2:
            self.find_element(By.XPATH, ".//*[@id='addTaskTable']/tbody/tr/td[4]/a").click()
            
    def dispaly_device_more_than_one(self, index):
        self.find_element(By.XPATH, ".//*[@id='addTaskTable']/tbody/tr[%s]/td[3]/a"%str(index)).click()
        
    #判断6台设备是否连接成功
    def get_device_num(self):
        device_tbody = self.find_element(*self.device_tbody_loc)
        device_row = device_tbody.find_elements(*self.device_row_loc)
        return len(device_row)

    #选择设备并保存
    def choose_device(self, i):
        i = i + 1
        if i > 1:
            display_device_i_loc = (By.CSS_SELECTOR, "#addTaskTable>tbody>tr:nth-child("+str(i)+")>td:nth-child(3)>a")
            self.find_element(*display_device_i_loc).click()
        select_device_loc = (By.CSS_SELECTOR, "#devices>tr:nth-child("+str(i)+")")
        self.find_element(*select_device_loc).click()
        self.find_element(*self.save_device_loc).click()
    
    def input_run_time(self, index):
        if index == 1:
            self.find_element(By.XPATH, ".//*[@id='addTaskTable']/tbody/tr/td[5]/input[1]").clear()
            self.find_element(By.XPATH, ".//*[@id='addTaskTable']/tbody/tr/td[5]/input[1]").send_keys("20")
        else:
            self.find_element(By.XPATH, ".//*[@id='addTaskTable']/tbody/tr[%s]/td[5]/input[1]"%str(index)).clear()
            self.find_element(By.XPATH, ".//*[@id='addTaskTable']/tbody/tr[%s]/td[5]/input[1]"%str(index)).send_keys("20")

    #点击选择脚本
    def select_scripts(self):
        self.find_element(*self.scripts_loc).click()

    #添加脚本并保存
    def add_scripts_save(self):
        self.find_element(*self.add_scripts_loc).click()
        if type:
            self.find_element(*self.save_scripts_loc).click()

    #添加新的device
    def add_new_device(self, i):
        if i == 1:
            self.find_element(*self.add_new1_loc).click()
        else:
            add_new_loc = (By.XPATH, "//*[@id='addTaskTable']/tbody/tr["+str(i)+"]/td[8]/a[2]/span")
            self.find_element(*add_new_loc).click()

    #保存所添加的设备和脚本
    def save_confirm(self):
        self.find_element(*self.save_task_loc).click()
        self.find_element(*self.confirm_task_loc).click()

    #判断是否创建成功
    def wait_task_excute(self):
        if self.find_element(*self.wait_task_loc):
            return True

    #脚本数量显示
    def scripts_num_display(self):
        var = Select(self.find_element(*self.scripts_num_loc))
        var.select_by_visible_text("25")

    #点击下一步选择模块
    def select_module(self):
        self.find_element(*self.next_loc).click()
        self.find_element(*self.choose_module_loc).click()
        self.find_element(*self.choose_all_module_loc).click()

    def module_save(self):
        self.find_element(*self.save_module_loc).click()
        
    def run_tast(self):
        for i in range(15):
            if self.is_element_exits("//*[text()='等待下发']"):
                #下发
                self.find_element(By.XPATH, ".//*[@id='tableBody']/tr/td[7]/a[1]/img").click() 
                sleep(2)
                #确定
                self.find_element(By.XPATH, ".//*[@id='error_pop']/div[2]/p[2]/a[1]").click() 

            elif self.is_element_exits("//*[text()='下发成功']"):
                print 'Start'
                #启动
                self.find_element(By.XPATH, ".//*[@id='tableBody']/tr/td[7]/a[3]/img").click() 
                sleep(2)
                #确定
                self.find_element(By.XPATH, ".//*[@id='error_pop']/div[2]/p[2]/a[1]").click() 
                sleep(20)
                
            elif self.is_element_exits("//*[text()='正在下发']") or self.is_element_exits("//*[text()='正在启动']"):
                #刷新
                self.find_element(By.XPATH, ".//*[@id='queryBtn']/span").click() 
                sleep(5)
                
            elif self.is_element_exits("//*[text()='正在执行']"):
                print 'Running'
                break


    
    def choose_inter_test(self):
        self.find_element(By.XPATH, ".//*[@id='first']/div[4]/div/div/div/span[2]").click() 
        
    def choose_device_id(self, id):
        self.find_element(By.XPATH, "//*[text()='%s']"%id).click() 
        self.find_element(By.XPATH, ".//*[@id='saveDeviceBtn']/span[2]").click()
































