# -*- coding: utf-8 -*-
# *****************************************************************************
# Title:        04_Browser
# ******************************************************************************
from __future__ import division
from uiautomator import Device
import os, sys
import math
import traceback
import random
import common.common
from common.getconfigs import GetConfigs
import common.browser
import common.settings

logger = common.common.createlogger("MAIN")
logger.debug("Get some configurations")
cfg = GetConfigs("04_browser")
testplace = cfg.getstr("TestPlace", "TEST_PLACE", "common")

NetworkType = cfg.getstr("Default", "NETWORK_TYPE", "common")
logger.info("Test Network Type is " + NetworkType)

dicttest_times = cfg.get_test_times()
test_times = 0
suc_times = 0
NetworkType_split = NetworkType.split('/')
lenght = len(NetworkType_split)
for TestTime in dicttest_times:
    for i in range(lenght):
        if TestTime.upper().find(NetworkType_split[i].upper()) > -1:
            test_times += int(dicttest_times[TestTime])

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
m_brow = common.browser.Browser(mdevice, "M_BROWSER")
m_settings = common.settings.Settings(mdevice, 'M_SETTINGS')

logger.info("Trace Total Times " + str(test_times))


def visit_default_page(key, network_type):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    switch = True
    if times:
        logger.debug('Use %s Visit default url %d Times.' % (network_type, times))
        if not key.find('WiFi') > -1:
            switch = m_settings.switch_network(network_type, os.environ.get("MDEVICE"))
        for loop in range(times):
            try:
                if switch and m_brow.stay_in_browser():
                    if m_brow.select_bookmark('1'):
                        suc_times = suc_times + 1
                        logger.info("Trace Success Loop %s." % (loop + 1))
                        m_brow.clear_data()
                    else:
                        m_brow.save_fail_img()
            except Exception, e:
                m_brow.save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug("Visit default url Test Finished.")


def navigation(key, network_type):
    global suc_times
    if testplace == 'US':
        URL = "http://www.google.com"
    else:
        #         URL = "http://122.225.253.188/"
        URL = "http://www.baidu.com"
    times = int(dicttest_times.get(key.lower(), 0))
    switch = True
    if times:
        logger.debug('Use %s Navigation %d Times.' % (network_type, times))
        if not key.find('WiFi') > -1:
            switch = m_settings.switch_network(network_type, os.environ.get("MDEVICE"))
        for loop in range(times):
            if switch and m_brow.stay_in_browser():
                try:
                    if not m_brow.browse_webpage(URL):
                        m_brow.save_fail_img()
                    else:
                        if testplace == 'US':
                            suc_times = suc_times + 1
                            logger.info("Trace Success Loop %s." % (loop + 1))
                            m_brow.clear_data()
                        else:
                            if URL == 'http://122.225.253.188/':
                                # mdevice.shell_dos("adb -s " +  os.environ.get("MDEVICE") + " shell input tap 70 207")
                                mdevice(description='Browser test/').click()
                            elif URL == 'http://www.baidu.com':
                                if mdevice(resourceId='login').exists:
                                    mdevice(resourceId='login').click()
                                else:
                                    mdevice.click(670, 197)
                                    if m_brow.is_loading(300) and mdevice(textContains='m.baidu.com').exists:
                                        mdevice.click(590, 199)
                                mdevice.delay(2)
                            else:
                                logger.debug('Unkonw URL!!!')
                                m_brow.save_fail_img()
                                break
                            mdevice.delay(2)
                            if not m_brow.is_loading(300):
                                logger.debug('Loading the fist link page fail')
                                m_brow.save_fail_img()

                            if (URL == 'http://www.baidu.com' and mdevice(textContains='个人中心').exists) \
                                    or (URL == 'http://122.225.253.188/' and mdevice(textContains='Browser').exists):
                                suc_times = suc_times + 1
                                logger.info("Trace Success Loop %s." % (loop + 1))
                                m_brow.clear_data()
                            else:
                                logger.debug('Open the fist link page fail')
                                m_brow.save_fail_img()
                except Exception, e:
                    m_brow.save_fail_img()
                    common.common.log_traceback(traceback.format_exc())
        logger.debug("Navigation Test Finished.")


def top_web(key, network_type):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    switch = True
    if times:
        logger.debug('Use %s Top Web %d Times.' % (network_type, times))
        if not key.find('WiFi') > -1:
            switch = m_settings.switch_network(network_type, os.environ.get("MDEVICE"))
        for loop in range(times):
            success = 0
            select_times = 0
            if switch and m_brow.stay_in_browser():
                try:
                    for i in range(1, 6):
                        if m_brow.select_bookmark(i):
                            select_times += 1
                            logger.debug('load bookmark %s successfully!', select_times)
                            success += 1
                        else:
                            m_brow.save_fail_img()
                            logger.debug('load bookmark %s fail!', select_times)
                            m_brow.stay_in_browser()
                    if success >= 5:
                        suc_times = suc_times + 1
                        logger.info("Trace Success Loop %s." % (loop + 1))
                    m_brow.clear_data()
                except Exception, e:
                    m_brow.save_fail_img()
                    common.common.log_traceback(traceback.format_exc())
        logger.debug("Topweb Test Finished.")


def main():
    global network_type
    mdevice.watcher("NO Thanks").when(text='NO, THANKS').click(text="NO, THANKS")
    logger.debug("Start Browser Test.")

    if NetworkType.find('WiFi') > -1:
        SSID = cfg.getstr("Wifi", "wifi_name", "common")
        PWD = cfg.getstr("Wifi", "wifi_password", "common")

    if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
        #     if NetworkType.find('WiFi') > -1 :
        visit_default_page('FirstPageWiFi', 'WiFi')
    #     if NetworkType.find('2G') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         visit_default_page('FirstPage2G', '2G')
    #     if NetworkType.find('3G') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         visit_default_page('FirstPage3G', '3G')
    #     if NetworkType.find('LTE') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         visit_default_page('FirstPageLTE', 'LTE')
    #     if NetworkType.find('All') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         visit_default_page('FirstPageAll', 'All')
    #
    if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
        #     if NetworkType.find('WiFi') > -1 :
        navigation('NavigateWiFi', 'WiFi')
    # if NetworkType.find('2G') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         navigation('Navigate2G', '2G')
    #     if NetworkType.find('3G') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         navigation('Navigate3G', '3G')
    #     if NetworkType.find('LTE') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         navigation('NavigateLTE', 'LTE')
    #     if NetworkType.find('All') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         navigation('NavigateAll', 'All')
    #
    if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
        #     if NetworkType.find('WiFi') > -1 :
        top_web('TopSitesWiFi', 'WiFi')
    #     if NetworkType.find('2G') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         top_web('TopSites2G', '2G')
    #     if NetworkType.find('3G') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         top_web('TopSites3G', '3G')
    #     if NetworkType.find('LTE') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         top_web('TopSitesLTE', 'LTE')
    #     if NetworkType.find('All') > -1 and m_settings.set_wifi_close("MDEVICE"):
    #         top_web('TopSitesAll', 'All')
    #
    m_brow.exit_browser()
    logger.debug("Browser Test Finished.")
    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
# Scrpit End
