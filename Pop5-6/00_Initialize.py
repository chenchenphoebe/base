# Title:        Initialize_Device
# Precondition: 1.One device connect
# Description:  Initialize device before test
# Platform:     Android 7.0
# Project:      Pixi5-10 VDF
# author:       Han Bei
# *****************************************************************************
from __future__ import division
from uiautomator import Device
import sys
import os
import traceback
import common.common
from common.getconfigs import GetConfigs
import common.initialize

FilePathFile = sys.path[0]+"\\ResourceFile\\PicComparison\\TestFile\\Contacts_51-100.vcf"
FilePathApk = sys.path[0]+"\\ResourceFile\\PicComparison\\TestFile\\AutoFillTest.apk"
FilePathMusic = sys.path[0]+"\\ResourceFile\\PicComparison\\TestFile\\Music"
FilePathPictures = sys.path[0]+"\\ResourceFile\\PicComparison\\TestFile\\Pictures"
FilePathMessage = sys.path[0]+"\\ResourceFile\\PicComparison\\TestFile\\Message"
FilePathMovies = sys.path[0]+"\\ResourceFile\\PicComparison\\TestFile\\Movies"
logger = common.common.createlogger('MAIN')
logger.debug('connect device')
mdevice = common.common.connect_device('MDEVICE')
m_init = common.initialize.Initialize(mdevice, "M_INITIALIZE")

suc_times = 0
cfg = GetConfigs("")

email_password = 'mobile#3'
environ = os.environ
device_id = environ.get('MDEVICE')
logger.debug("Device ID is " + device_id)
email_dict = {'RCN7FAIRVSPRHAGA': 'szautotest07@tcl.com', 'EIZT75BM8DBQHEUW': 'szautotest08@tcl.com',
              'KNF6KJQWJBL7PBUK': 'szautotest09@tcl.com', 'CMOF6HRSZSNZ9LI7': 'szautotest10@tcl.com',
              'FEFYDM5TVWOV6D5D': 'szautotest11@tcl.com', 'CIAAOBPZ5PGIOR5H': 'szautotest12@tcl.com'}

internal_storage_name = 'Internal storage'
environ = os.environ
device_id = environ.get('MDEVICE')
mdevice.shell_adb('-s ' + device_id + ' push ' + '"' + FilePathFile + '"' + ' /sdcard/')
mdevice.shell_adb('-s ' + device_id + ' push ' + '"' + FilePathApk + '"' + ' /sdcard/')
mdevice.shell_adb('-s ' + device_id + ' push ' + '"' + FilePathMusic + '"' + ' /sdcard/')
mdevice.shell_adb('-s ' + device_id + ' push ' + '"' + FilePathPictures + '"' + ' /sdcard/')
mdevice.shell_adb('-s ' + device_id + ' push ' + '"' + FilePathMessage + '"' + ' /sdcard/')
mdevice.shell_adb('-s ' + device_id + ' push ' + '"' + FilePathMovies + '"' + ' /sdcard/')

def Display_SleepMode():
    global suc_times
    logger.debug('set the sleep mode to \'Never\'')
    if m_init.wakeupAunlock():
        if m_init.enterSettings('Display') and m_init.set_sleep_mode('Never'):
            logger.debug('set the sleep mode to \'Never\' success')
            mdevice.press.home()
            suc_times += 1
            logger.info("Trace Success Loop 1.")
            return True
    logger.debug('set the sleep mode to \'Never\' fail')
    m_init.save_fail_img()
    mdevice.press.home()
    return False


def Default_Settings():
    global suc_times
    logger.debug('set the Brightness && Sound to \'Minimal\' ')
    if m_init.enterSettings('Display'):
                # m_init.Min_Brightness()
        logger.debug('set the Brightness_level to \'Minimal\' ')
        mdevice.press.home()
        if m_init.enterSettings('Sound'):
            m_init.Min_Volume()
            logger.debug('set the Sound to \'Minimal\' ')
            mdevice.press.home()
        suc_times += 1
        logger.info("Trace Success Loop 1.")
        return True
    logger.debug('set the sleep mode to \'Never\' fail')
    m_init.save_fail_img()
    mdevice.press.home()
    return False


def Conect_wifi():
    global suc_times
    SSID = cfg.getstr("Wifi", "wifi_name", "common")
    PWD = cfg.getstr("Wifi", "wifi_password", "common")
    if m_init.enterSettings('Wi-Fi') and m_init.turn_wifi_on() and m_init.connect_wifi(SSID, PWD):
        logger.debug('Connected wifi with %s', SSID)
        mdevice.press.home()
        suc_times += 1
        logger.info("Trace Success Loop 1.")
        return True
    logger.debug('set the sleep mode to \'Never\' fail')
    m_init.save_fail_img()
    mdevice.press.home()


def Add_chrome_Bookmark():
    global suc_times
    logger.debug('Add bookmarks for the chrome')
    suc = 0
    bookmarks = ['www.baidu.com', 'www.jd.com', 'www.hao123.com', 'www.taobao.com', 'www.163.com']
    if m_init.enter_chrome():
        try:
            for mark in bookmarks:
                logger.debug('Add bookmark:' + mark)
                if m_init.add_bookmarks(mark):
                    suc += 1
                    logger.debug('Add bookmark:' + mark + 'successfully')
                else:
                    logger.debug('Add bookmark:' + mark + 'fail')
            mdevice.press.home()
        except Exception, e:
            logger.debug('Fail to enter_chrome')
            m_init.save_fail_img()
            common.common.log_traceback(traceback.format_exc())
            mdevice.press.home()
    else:
        m_init.save_fail_img()
    mdevice.press.home()
    if suc == len(bookmarks):
        logger.debug('Add all bookmark success')
        suc_times += 1
        logger.info("Trace Success Loop 1.")
        return True
    return False


def Add_browser_Bookmark():
    global suc_times
    logger.debug('Add bookmarks for the broswer')
    suc = 0
    bookmarks = ['www.baidu.com', 'www.jd.com', 'www.hao123.com', 'www.taobao.com', 'www.163.com']
    if m_init.stay_in_browser():
        try:
            for mark in bookmarks:
                logger.debug('Add broswer bookmark:' + mark)
                if m_init.add_browser_bookmarks(mark):
                    suc += 1
                    logger.debug('Add broswer bookmark:' + mark + 'successfully')
                else:
                    logger.debug('Add broswer bookmark:' + mark + 'fail')
            mdevice.press.home()
        except Exception, e:
            logger.debug('Fail to enter_broswer')
            m_init.save_fail_img()
            common.common.log_traceback(traceback.format_exc())
            mdevice.press.home()
    else:
        m_init.save_fail_img()
    mdevice.press.home()
    if suc == len(bookmarks):
        logger.debug('Add all bookmark success')
        suc_times += 1
        logger.info("Trace Success Loop 1.")
        return True
    return False


def Import_Contacts():
    global suc_times
    logger.debug('import the contact into storage')
    mdevice.delay(2)
    if m_init.import_contact('Contacts_51-100.vcf'):
        logger.debug('import contact from storage successfully')
        mdevice.press.back()
        suc_times += 1
        logger.info("Trace success Loop 1")
        return True
    mdevice.press.home()
    return False


def Login_Email():
    global suc_times
    logger.debug('login email account')
    if m_init.email_accountSet(email_dict[device_id], email_password):
        mdevice.press.home()
        suc_times += 1
        logger.info('Trace success Loop 1')
        return True
    mdevice.press.home()
    return False


def Add_Message_Draft():
    global suc_times
    logger.debug('Add 4 messages drafts')
    content = 'sdjahfdjakfhdajkfhajkdhfldshalfhfhfhfhhfhfhfhfhfhfhhffhhfhfhfhfhhfhfhfhfhfhhfhfhshshshhshshshshshhshshshshsshshshhsdsdsfsfsfsdfsdfsf'
    Draft_num = 0
    if m_init.stay_in_messaging():
        i = 0
        msg_type = ['Text', 'Picture', 'Video', 'Audio']
        No_list = ['0', '1', '2', '3']
        for Type in msg_type:
            logger.debug('Add %s type message', Type)
            if m_init.save_msg(content, Type, No_list[i]):
                m_init.send_saveMsg(Type)
                Draft_num += 1
            else:
                m_init.save_fail_img()
                break
            i += 1
            m_init.back_to_message()
    if Draft_num == 4:
        logger.debug('Add 4 message drafts successfully')
        suc_times += 1
        logger.info('Trace success loop 1')
        return True
    logger.debug('Add 4 messages fail')
    return False


def Delete_Message_File():
    global suc_times
    logger.debug('Delete the message file from file manager')
    if m_init.stay_in_filemanger() and m_init.open_path(internal_storage_name) and m_init.delete_item('Message'):
        logger.debug('Delete the msg file successfully')
        suc_times += 1
        logger.info('Trace success Loop 1')
        mdevice.press.home()
        return True
    else:
        m_init.save_fail_img()
        return False


def main():
    Display_SleepMode()
    Default_Settings()
    Conect_wifi()
    # # Add_chrome_Bookmark()
    Add_browser_Bookmark()
    # # Import_Contacts()
    Login_Email()
    Add_Message_Draft()
    Delete_Message_File()


if __name__ == "__main__":
    main()
# Scrpit End
