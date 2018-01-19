#-*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import division

from datetime import datetime
import logging
import os
import random
import re
import sys
import time
import traceback
import unittest

from getconfigs import GetConfigs
from uiautomator import Device


def createlogger(name):
    logger = logging.getLogger(name)
    logger.setLevel("DEBUG")
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d: [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s',
        '%y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
logger = createlogger("COMMON")


def create_folder():
    log_path=os.environ.get("LOG_PATH")
    if log_path is None:
        log_path = sys.path[0][sys.path[0].find(':')+1:] + '\\results'#find()找不到则返回-1
        print log_path
    if not os.path.exists(log_path):
        logger.debug("log_path not exsit")
        os.makedirs(log_path)
    if not os.path.exists(log_path):
        return None
    return log_path

def log_traceback(traceback):
    str_list=traceback.split("\n")
    for string in str_list:
        logger.warning(string)

def connect_device(device_name):
    environ = os.environ
    device_id = environ.get(device_name)
    logger.debug("Device ID is " + device_id)
    device = Device(device_id)
    if device is None:
        logger.critical("Cannot connect device.")
        raise RuntimeError("Cannot connect %s device." % device_id)
    return device

def runTest(testCaseClass, cases=[]):
    suite = unittest.TestSuite()
    if cases:
        for c in cases:
            suite.addTest(testCaseClass(c))
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(testCaseClass)
    unittest.TextTestRunner().run(suite)

class Common(object):
    '''common 类'''
    def __init__(self, device,log_name):
        self._device = device
        self._logger = createlogger(log_name)
        self._log_path = create_folder()
        self._config = GetConfigs("common")

    def save_img(self, folder):
        path_split = self._log_path.split('\\')
        lenght = len(path_split)
        pic_path = ''
        for i in range(lenght):
            if path_split[i].find('TCTS') > -1:
                if os.path.isdir(pic_path + path_split[i] + '\\Error_snap' + '\\') == False:
                    os.mkdir(pic_path + path_split[i] + '\\Error_snap' + '\\')
                pic_path = pic_path + path_split[i] + '\\Error_snap' + '\\' + folder + '\\'
                if os.path.isdir(pic_path) == False:
                    os.mkdir(pic_path)
                break
            else:
                pic_path = pic_path + path_split[i] + '\\'
            path = (pic_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
            newimg = None
            self._logger.debug("Take snapshot.")
            newimg = self._device.screenshot(path)
            if newimg is None:
                self._logger.warning("Add picture is None.")
                return False
            self._logger.error("Fail: %s" % (path))
            return True

    def get_file_num(self, path, format):
        '''shell_adb不存在！！！！！'''
        content = self._device.shell_adb("shell ls " + path)
        num = 0
        for i in range(len(format)):
            num += content.count(format[i])
        self._logger.debug("%s file num is %d." % (format, num))
        return num

    def enter_app(self, name):
        launcher_name = self.get_app_package_from_file("Launcher")
        if self._device(text=name).exists:
            if not ((self._device(resourceId=launcher_name + ':id/hotseat').child(description='Apps').exists \
                     or self._device(description='apps').exists \
                     or self._device(description='ALL APPS').exists) and (
                    name == 'Mix' or name == 'Music' or name == "Sound Recorder" or name == "Radio")):
                self._logger.debug("enter " + name + " in current page")
                self._device(text=name).click()
                self._device.delay(2)
                return True

        if not(self._device(resourceId = launcher_name +':id/hotseat').child(description='Apps').exists or self._device(description='apps').exists\
         or self._device(description='ALL APPS').exists):
            self._device.press.home()
            self._device.delay(2)
            if self._device(text=name).exists and name <> 'Mix' and name <> 'Music' and name <> "Sound Recorder" and name <> "Radio":
                self._logger.debug("enter " + name + " in home page")
                self._device(text=name).click()
                self._device.delay(2)
                return True

        if self._device(resourceId=launcher_name + ':id/hotseat').child(
                description='Apps').exists or self._device(description='apps').exists \
                or self._device(description='ALL APPS').exists:
            self._logger.debug("enter Apps")
            if self._device(resourceId=launcher_name + ':id/layout').child(description='Apps').exists:
                self._device(resourceId=launcher_name + ':id/layout').child(description='Apps').click()
                self._logger.debug('Enter main screen successfully')
            elif self._device(description='ALL APPS').exists:
                self._device(description='ALL APPS').click()
                self._logger.debug('Enter main screen successfully')
            else:
                self._device(description='apps').click()
            self._device.delay(2)

            if self._device(resourceId=launcher_name + ':id/apps_list_view').child_by_text(name).exists:
                self._logger.debug("enter " + name)
                self._device(text=name).click()
                self._device.delay(2)
                return True;
            else:
                self._logger.debug("Didn't search" + name)
                return False
        else:
            self._logger.debug("Didn't search Apps")
            self.clear_all_app()
            if self.enter_app(name):
                return True
            return False

    def clear_all_app(self):
        self._device.shell_adb('shell input keyevent 187')
        self._device.delay(1)
        if self._device(text='No recent items').wait.exists(timeout=1000):
            self._logger.debug('No recent items')
            self._device.press.back()
            return True
        for i in range(10):
            if not self._device(resourceId="com.android.systemui:id/button",text='CLEAR ALL').wait.exists(timeout=1000):
                self._device(scrollable=True).scroll.toBeginning(steps=10)
            else:
                break
        self._device(resourceId="com.android.systemui:id/button",text='CLEAR ALL').click()
        self._device.delay(3)
        self._logger.debug('clear all app is success!!')
        return True

    def get_current_packagename(self):
        """get the packagename display now

        """
        info = self._device.info
        return info[u'currentPackageName']

    def get_app_package_from_file(self,app_name):
        file = open(sys.path[0]+"\\common\\AppInfo.txt",mode="r")
        line=file.readline()
        while line <> "":
            if line.find('['+ app_name+']') <> -1:
                find_id = file.readline().strip()
                if find_id.find('/') > -1:
                    return find_id[:find_id.index('/')]
            else:
                line = file.readline()
        file.close()
        return False

    def if_data_connected(self, device_id):
        '''shell_dos函数运用'''
        result = self._device.shell_dos('adb -s ' + device_id + ' shell ifconfig rmnet_data0')
        if result.find('Scope: Link') > -1:
            self._logger.debug("Data is connected.")
            return True
        else:
            self._logger.debug("No data connected.")
            return False

    def random_number(self, len):
        numseed = "0123456789"
        logger.debug('Create a random name.')
        sa = []
        for i in range(len):
            sa.append(random.choice(numseed))
        return ''.join(sa)#返回字符串

    def clear_recent(self):
        self._logger.debug("clear_recent")
        self._device.press.recent()
        self._device.delay(2)
        if self._device(text="CLEAR ALL").wait.exists(timeout=2000):
            self._device(text="CLEAR ALL").click()
            self._device.delay(3)
            return True
        elif self._device(resourceId="com.android.systemui:id/dismiss_task").wait.exists(timeout=2000):
            self._device(resourceId="com.android.systemui:id/dismiss_task").click()
            self._device.delay(3)
            return True
        else:
            self._device.press.back()
            return True

    def back_to_home(self):
        maxloop = 0
        while not self._device(description='ALL APPS').exists:
            self._device.press.back()
            self._device.delay(2)
            if maxloop > 10:
                break
            maxloop += 1






