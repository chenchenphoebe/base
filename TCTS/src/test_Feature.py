# -*- coding: utf-8 -*-
__author__ = 'hanbei'
import sys
import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from common.log import log
from common.create_plan import Create_Plan
from common.create_scripts import Create_Scripts
from common.create_project import Create_project
from common.create_task import Create_task
from common.lock_project import Lock_project
from common.login_tcloud import Login_tcloud
from common.getconfigs import GetConfigs
from common.globalparameter import test_plan
from common.globalparameter import test_task

cfg = GetConfigs()
username = cfg.getstr("Login", "username", "common")
password = cfg.getstr("Login", "password", "common")
test_project = cfg.getstr("TestProject", "test_project", "common")
vpm = cfg.getstr("TestProject", "vpm", "common")
PC_name = cfg.getstr("TestPC", "pc_name", "common")
MDevice = cfg.getstr("TestDevice", "mdevice", "common")
SDevice = cfg.getstr("TestDevice", "sdevice", "common")
SW_version = cfg.getstr("TestVersion", "maincode", "common")
Perso_version = cfg.getstr("TestVersion", "perso", "common")
Tester = cfg.getstr("Tester", "tester", "common")
modules_name = ["01_Launcher", "03_Network", "04_Wifi", "05_Bluetooth", "06_Settings", "08_Contacts", "09_Messaging", \
                "10_Email.py", "11_Chrome&&Browser", "12_Camera", "13_Gallery", "14_Filemanager", "15_SoundRecoder",\
                "16_Call", "20_Time", "21_Multimedia"]


class TestMTBF(unittest.TestCase):
    def setUp(self):
        binary = FirefoxBinary(r'D:\firefox-sdk\bin\firefox.exe')
        self.driver = webdriver.Firefox()
        self.url = 'http://10.128.161.36/mobileTestCenter/login.jsp'
        self.keyword = 'TAT3.0'
        self.login = Login_tcloud(self.driver, self.url, u"TCloud Test System | 登录")
        self.project = Create_project(self.driver, self.url, u"项目管理")
        self.lock = Lock_project(self.driver, self.url, u"锁定项目")
        self.plan = Create_Plan(self.driver, self.url, u"创建Plan")
        self.scripts = Create_Scripts(self.driver, self.url, u"添加脚本")
        self.task = Create_task(self.driver, self.url, u"创建任务")

        self.logger = log()

    """
    测试Feature主要操作步骤
    """

    def test_Feature(self):
        self.login_cloud()
        self.create_project()
        self.lock_project()
        self.Feature_plan()
        self.Feature_scripts()
        self.create_task()
        self.run_tast()
    """
    登录T-cloud
    """
    def login_cloud(self):
        try:
            self.login.open()
            self.login.input_username(username)
            self.login.input_password(password)
            beforehandle = self.driver.current_window_handle
            self.logger.debug(beforehandle)
            self.login.choose_site()
            self.login.click_login()
            sleep(2)
            self.assertIn(self.keyword, self.driver.title)
            self.logger.debug("complete login")
        except Exception as e:
            self.login.img_screenshot(u'登录')
            raise e

    """
    创建项目
    """

    def create_project(self):

        try:
            print "begin to create project"
            self.project.project_manage()
            self.project.increase_button()
            self.project.input_project(test_project)
            self.project.choose_project()
            self.project.input_vpm(vpm)
            self.project.input_vpmEmail(vpm + "@tcl.com")
            self.project.save_project()
            self.project.confirm_project()
        except Exception as e:
            self.project.img_screenshot(u'创建项目')
            raise e

    """
    锁定项目
    """

    def lock_project(self):
        try:
            print "begin to lock the project"
            self.lock.lock()
            self.lock.click_project()
            project_name = self.lock.get_project_name()
            if project_name == test_project:
                print "lock project successfully"
            else:
                raise NameError("lock project error")
        except Exception as e:
            self.lock.img_screenshot(u'锁定项目')
            raise e

    """
        创建计划
    """

    def Feature_plan(self):
        try:
            print "begin to create the plan"
            self.plan.click_plan_manage()
            self.plan.click_Feature_plan()
            self.plan.click_add_icon()
            self.plan.input_plan_name(test_plan)
            self.plan.input_SW_version(SW_version)
            self.plan.input_perso_version(Perso_version)
            self.plan.tester(Tester)
            self.plan.tester_email(Tester + "@tcl.com")
            self.plan.test_report()
            self.plan.recipient_email(Tester + "@tcl.com")
            self.plan.cc_email(Tester + "@tcl.com")
            self.plan.email_subject(test_project + "(" + SW_version + "+" + Perso_version + ")" + "Feature Test")
            self.plan.email_content(test_project + " " + "Feature  Test complete, The attachment is test report")
            self.plan.save_plan()
            self.plan.confirm()
        except Exception as e:
            self.plan.img_screenshot(u'创建测试计划')
            raise e
    """
    添加模块脚本
    """
    def Feature_scripts(self):
        self.scripts.manage_module()
        self.scripts.scripts_num_display()
        module_num = self.scripts.current_scripts_sum()
        try:
            if module_num == 16:
                suc_time = 0
                for j in range(module_num):
                    module_name = self.scripts.get_scripts_name(j, "0")
                    print module_name
                    if module_name in modules_name:
                        suc_time += 1
                        if suc_time == 16:
                            print "module add successfully"
                    else:
                        print "module are added error"
                        return False
            elif 1 < module_num < 16 or module_num > 16:
                return False
            elif module_num == 1:
                self.add_modules()
        except Exception as e:
            self.scripts.img_screenshot(u'添加脚本')
            raise e

    # def delete_all_modules(self, module_num):
    #     try:
    #         print "delete the all module"
    #         self.scripts.delete_module(module_num)
    #     except Exception as e:
    #         self.scripts.img_screenshot(u'删除模块')
    #         raise e

    def add_modules(self):
        try:
            print "add all the modules"
            self.scripts.add_SVN_module()
            self.scripts.module_SVN_address()
            #判断是否添加成功
            self.scripts.scripts_num_display()
            module_num = self.scripts.current_scripts_sum()
            if module_num == 16:
                print "module add successfully"
            else:
                print "module add fail"
                return False
        except Exception as e:
            self.scripts.img_screenshot(u'添加模块')
            raise e

    """
        创建task
        """

    def create_task(self):
        click_times = 0
        self.plan.click_plan_manage()
        self.plan.click_Feature_plan()
        while not self.task.plan_exists():
            self.plan.click_Feature_plan()
            click_times += 1
            if click_times == 5:
                return False
        self.task.click_plan()
        self.task.add_task(test_task)
        sleep(2)
        print '------'
        self.task.PC_name(PC_name)
        print '------'
        self.task.choose_inter_test()
        self.task.clear_timeout()
        
        self.task.display_device(1)
        device_num = self.task.get_device_num()
        if device_num >= 2:
            print "all device is ready"
        else:
            print "the device shortage"
            self.task.img_screenshot(u'查看设备数目显示')
            return False
        
        self.task.choose_device_id(MDevice)
        sleep(2) 
        
        self.task.display_device(2)
        device_num = self.task.get_device_num()
        if device_num >= 2:
            print "all device is ready"
        else:
            print "the device shortage"
            self.task.img_screenshot(u'查看设备数目显示')
            return False
        self.task.choose_device_id(SDevice)
        sleep(2) 

        # 每台设备添加相应的脚本
#         for i in range(2):
#             print i
#             if i > 0:
#                 self.task.add_new_device(i)
#                 sleep(2)
#             self.task.choose_device(i)
#             print "choose device successfully"
#             sleep(3)
        #添加模块
        self.task.select_module()
        sleep(2)
        self.task.module_save()
        print "completecompletecompletecomplete"
        # # 完成设备和脚本的添加
        self.task.save_confirm()
        # # 判断任务是否添加成功
        try:
            if self.task.wait_task_excute():
                print "create task succeessfully"
            else:
                print "create task fail"
        except:
            self.task.img_screenshot(u"判断创建任务是否成功")
            
    def run_tast(self):
        self.task.run_tast()

    def tearDown(self):
#         self.driver.close()
        print "Finish"
        
if __name__ == "__main__":
    unittest.main()