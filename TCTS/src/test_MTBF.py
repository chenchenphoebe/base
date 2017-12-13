# -*- coding: utf-8 -*-
#encoding:utf8
__author__ = 'helen'
import sys
import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from common.getconfigs import GetConfigs
from common.log import log
from common.create_plan import Create_Plan
from common.create_scripts import Create_Scripts
from common.create_project import Create_project
from common.create_task import Create_task
from common.lock_project import Lock_project
from common.login_tcloud import Login_tcloud
from common.globalparameter import test_plan
from common.globalparameter import test_task
from selenium.webdriver.common.by import By

cfg = GetConfigs()
username = cfg.getstr("Login", "username", "common")
password = cfg.getstr("Login", "password", "common")
test_project = cfg.getstr("TestProject", "test_project", "common")
vpm = cfg.getstr("TestProject", "vpm", "common")
PC_name = cfg.getstr("TestPC", "pc_name", "common")
SW_version = cfg.getstr("TestVersion", "maincode", "common")
Perso_version = cfg.getstr("TestVersion", "perso", "common")
Tester = cfg.getstr("Tester", "tester", "common")
scripts_name = [
#                 "00_Initialize.py", 
                "01_Telephony.py", "02_Messaging.py", "03_Email.py", "04_Browser.py", "05_PIM.py", \
                "06_Multi-Media.py", "07_Multi Tasking.py", "08_Menu_Navigation.py", "09_Settings.py",
                "10_Filemanager.py"]

DeviceID = []
Device1 = cfg.getstr("TestDevice", "device1", "common")
DeviceID.append(Device1)
Device2 = cfg.getstr("TestDevice", "device2", "common")
DeviceID.append(Device2)
Device3 = cfg.getstr("TestDevice", "device3", "common")
DeviceID.append(Device3)
Device4 = cfg.getstr("TestDevice", "device4", "common")
DeviceID.append(Device4)
Device5 = cfg.getstr("TestDevice", "device5", "common")
DeviceID.append(Device5)
Device6 = cfg.getstr("TestDevice", "device6", "common")
DeviceID.append(Device6)



class TestMTBF(unittest.TestCase):
    def setUp(self):
        binary = FirefoxBinary(r'D:\firefox-sdk\bin\firefox.exe')
        self.driver = webdriver.Firefox(firefox_binary=binary)
        self.url = 'http://10.128.161.36/mobileTestCenter/login.jsp'
        self.keyword = 'TAT3.0'
        self.login = Login_tcloud(self.driver, self.url, u"TCloud Test System | 鐧诲綍")
        self.project = Create_project(self.driver, self.url, u"椤圭洰绠＄悊")
        self.lock = Lock_project(self.driver, self.url, u"閿佸畾椤圭洰")
        self.plan = Create_Plan(self.driver, self.url, u"鍒涘缓Plan")
        self.scripts = Create_Scripts(self.driver, self.url, u"娣诲姞鑴氭湰")
        self.task = Create_task(self.driver, self.url, u"鍒涘缓浠诲姟")

        self.logger = log()

    """
    娴嬭瘯MTBF涓昏鎿嶄綔姝ラ
    """

    def test_Feature(self):
        self.login_cloud()
        self.create_project()
        self.lock_project()
        self.MTBF_plan()
        self.MTBF_scripts()
        self.create_task()
        self.run_tast()

    """
    鐧诲綍T-cloud
    """

    def login_cloud(self):
        try:
            self.login.open()
            self.login.input_username(username)
            self.login.input_password(password)
            # beforehandle = self.driver.current_window_handle
            # self.logger.debug(beforehandle)
            self.login.choose_site()
            self.login.click_login()
            sleep(2)
            self.assertIn(self.keyword, self.driver.title)
            self.logger.debug("complete login")
        except Exception as e:
            self.login.img_screenshot(u'鐧诲綍')
            raise e

    """
           鍒涘缓椤圭洰
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
            self.project.img_screenshot(u'鍒涘缓椤圭洰')
            raise e

    """
    閿佸畾椤圭洰
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
            self.lock.img_screenshot(u'閿佸畾椤圭洰')
            raise e
    """
    鍒涘缓璁″垝
    """
    def MTBF_plan(self):
        try:
            print "begin to create the plan"
            self.plan.click_plan_manage()
            self.plan.click_MTBF_plan()
            self.plan.click_add_icon()
            self.plan.input_plan_name(test_plan)
            self.plan.input_SW_version(SW_version)
            self.plan.input_perso_version(Perso_version)
            self.plan.tester(Tester)
            self.plan.tester_email(Tester + "@tcl.com")
            self.plan.test_report()
            self.plan.recipient_email(Tester + "@tcl.com")
            self.plan.cc_email(Tester + "@tcl.com")
            self.plan.email_subject(test_project + "(" + SW_version + "+" + Perso_version + ")" + "MTBF Test")
            self.plan.email_content(test_project + " "+"MTBF Test complete, The attachment is test report")
            self.plan.save_plan()
            self.plan.confirm()
        except Exception as e:
            self.plan.img_screenshot(u'鍒涘缓娴嬭瘯璁″垝')
            raise e
    """
    娣诲姞鑴氭湰
    """
    def MTBF_scripts(self):
        self.scripts.manage_scripts()
        self.scripts.scripts_num_display()
        scripts_num = self.scripts.current_scripts_sum()
        if scripts_num == 10:
            suc_time = 0
            for j in range(scripts_num):
                script_name = self.scripts.get_scripts_name(j, "1")
                if script_name in scripts_name:
                    print script_name
                    suc_time += 1
                    if suc_time == 10:
                        print "scripts add successfully"
                else:
                    print "scripts are added error"
                    return False
        elif 1 < scripts_num < 10 or scripts_num > 10:
            self.delete_scripts()
            self.add_scripts()
        elif scripts_num == 1:
            if self.scripts.exists_one_scripts():
                print "exists one scripts"
                self.delete_scripts()
                self.add_scripts()
            else:
                self.add_scripts()

    def delete_scripts(self):
        try:
            print "delete the all scripts"
            self.scripts.select_all_scripts()
            self.scripts.delete_all_scripts()
            self.scripts.confirm_delete()
        except Exception as e:
            self.scripts.img_screenshot(u'鍒犻櫎鑴氭湰')
            raise e

    def add_scripts(self):
        try:
            print "add all the scripts"
            for i in range(10):
                self.scripts.add_script()
                self.scripts.input_name(scripts_name[i])
                print scripts_name[i]
                self.scripts.choose_file_type()
                self.scripts.scripts_path(scripts_name[i])
                self.scripts.common_path()
                self.scripts.save_scripts()
                self.scripts.scripts_num_display()
            scripts_num = self.scripts.current_scripts_sum()
            if scripts_num == 10:
                print "add scripts successfully"
            else:
                print "add scripts fail"
                return False


        except Exception as e:
            self.scripts.img_screenshot(u'娣诲姞鑴氭湰')
            raise e
    """
    鍒涘缓task
    """
    def create_task(self):
        click_times = 0
        while not self.task.plan_exists():
            self.task.click_MTBF_plan()
            click_times += 1
            if click_times == 5:
                return False
        self.task.click_plan()
        self.task.add_task(test_task)
        self.task.PC_name(PC_name)
        self.task.clear_timeout()
        self.task.display_device(1)
        device_num = self.task.get_device_num()
        if device_num >= 2:
            print str(device_num) +" device is ready"
        else:
            print "the device shortage"
            self.task.img_screenshot(u'鏌ョ湅璁惧鏁扮洰鏄剧ず')
            return False
        # 姣忓彴璁惧娣诲姞鐩稿簲鐨勮剼鏈�
        
        ifaddIndex = True
        print DeviceID
        for i in range(len(DeviceID)):
            if DeviceID[i] <> None and DeviceID[i] <> "":
                if i > 0:
                    self.task.add_new_device(i)
                    sleep(2)
                    self.task.dispaly_device_more_than_one(i+1)
                self.task.choose_device_id(DeviceID[i])
                ifaddIndex = False
                sleep(3)
                self.task.input_run_time(i+1)
                self.task.select_scripts()
                self.task.scripts_num_display()
                self.task.add_scripts_save()
                sleep(3)
                print "completecompletecompletecomplete"
            
        if ifaddIndex:
            for i in range(device_num):
                print i
                if i > 0:
                    self.task.add_new_device(i)
                    sleep(2)
                self.task.choose_device(i)
                print "choose device successfully"
                sleep(3)
                self.task.input_run_time(i+1)
                self.task.select_scripts()
                self.task.scripts_num_display()
                self.task.add_scripts_save()
                sleep(3)
                print "completecompletecompletecomplete"
        # 瀹屾垚璁惧鍜岃剼鏈殑娣诲姞
        self.task.save_confirm()
        # 鍒ゆ柇浠诲姟鏄惁娣诲姞鎴愬姛
        try:
            if self.task.wait_task_excute():
                print "create task succeessfully"
            else:
                print "create task fail"
        except:
            self.task.img_screenshot(u"鍒ゆ柇鍒涘缓浠诲姟鏄惁鎴愬姛")
            
    def run_tast(self):
        self.task.run_tast()

    def tearDown(self):
        print 'finish'
#         self.driver.close()

if __name__ == "__main__":
    unittest.main()
