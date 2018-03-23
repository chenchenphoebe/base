# -*- coding: UTF-8 -*-
# *****************************************************************************
# Title:        02_Messaging
# *****************************************************************************
from __future__ import division
from uiautomator import Device
import traceback
import os
import common.common
from common.getconfigs import GetConfigs
import common.settings
import common.message2

logger = common.common.createlogger("MAIN")

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
m_msg = common.message2.Message(mdevice, "M_MESSAGE")
m_settings = common.settings.Settings(mdevice, "M_SETTINGS")
cfg = GetConfigs("02_messaging")
SEND_TO_NUMBER = cfg.getstr("Message", "msg_receive_num", "common")
NetworkType = cfg.getstr("Default", "NETWORK_TYPE", "common")
logger.info("Network Type is " + NetworkType)

dicttest_times = cfg.get_test_times()
test_times = 0
suc_times = 0
NetworkType_split = NetworkType.split('/')
lenght = len(NetworkType_split)
for TestTime in dicttest_times:
    for i in range(lenght):
        if TestTime.upper().find(NetworkType_split[i].upper()) > -1:
            test_times += int(dicttest_times[TestTime])
    if TestTime.upper() == "OPENTIMES":
        test_times = test_times + int(dicttest_times[TestTime]) * 4
logger.info("Trace Total Times " + str(test_times))


def forward_msg(msg_type, key, network_type, wait_time):
    # forward_msg('Text', 'SMSWiFi', 'WiFi', 60)
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    switch = True
    if times:
        logger.debug("____________Send %s %s times." % (key, times))
        if not key.find('WiFi') > -1:
            switch = m_settings.switch_network(network_type, os.environ.get("MDEVICE"))

        for loop in range(times):
            try:
                del_times = 0
                while m_msg.stay_in_messaging() and m_msg.get_total_thread() > 4:
                    m_msg.delete_messaging_thread()
                    del_times += 1
                    if del_times > 10:
                        logger.debug("There are too many messagings.")
                        m_msg.save_fail_img()
                        break

                logger.debug("Select the message with %s." % (msg_type))

                if switch and m_msg.stay_in_messaging() and m_msg.select_messaging(
                        msg_type) and m_msg.forward_messaging(SEND_TO_NUMBER, wait_time):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop %s." % (loop + 1))
                else:
                    m_msg.save_fail_img()

            except Exception, e:
                m_msg.save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug("Send %s Msg Test complete." % msg_type)


def open_msg(msg_type, key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("____________Open %s %s Times." % (msg_type, times))
        for loop in range(times):
            try:
                del_times = 0
                while m_msg.stay_in_messaging() and m_msg.get_total_thread() > 4:
                    m_msg.delete_messaging_thread()
                    del_times += 1
                    if del_times > 5:
                        logger.debug("There are too many messagings.")
                        m_msg.save_fail_img()
                        break

                if m_msg.stay_in_messaging() and m_msg.select_messaging(msg_type) and m_msg.open_messaging(msg_type):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop %s." % (loop + 1))
                else:
                    logger.warning("Cannot open message with %s." % msg_type)
                    m_msg.save_fail_img()
            except Exception, e:
                m_msg.save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug("Open %s Msg Test complete." % msg_type)


def main():
    logger.debug('Start Messaging Test')

    if NetworkType.find('WiFi') > -1:
        SSID = cfg.getstr("Wifi", "wifi_name", "common")
        PWD = cfg.getstr("Wifi", "wifi_password", "common")

    #     if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
    forward_msg('Text', 'SMSWiFi', 'WiFi', 60)

    #
    #     if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
    forward_msg('Audio', 'AudioWiFi', 'WiFi', 300)

    #     if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
    forward_msg('Video', 'VideoWiFi', 'WiFi', 300)

    #     if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
    forward_msg('Photo', 'PicWiFi', 'WiFi', 300)

    open_msg('Audio', 'OpenTimes')
    open_msg('Video', 'OpenTimes')
    open_msg('Photo', 'OpenTimes')
    open_msg('Text', 'OpenTimes')

    logger.debug("Finished Messaging Test")
    print "Finished Messaging Test"

    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
# Scrpit End
