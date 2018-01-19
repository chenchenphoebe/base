# *****************************************************************************
# Title:        09_Settings
# *****************************************************************************
from __future__ import division
import traceback
import common.common
from uiautomator import Device
from common.settings import Settings

from common.getconfigs import GetConfigs

logger = common.common.createlogger("MAIN")

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
d1_set = common.settings.Settings(mdevice, "M_SETTINGS")

logger.debug("Get some configurations")
cfg = GetConfigs("09_settings")
NetworkType = cfg.getstr("Default", "NETWORK_TYPE", "common")
logger.info("Network Typr is " + NetworkType)
SSID = cfg.getstr("Wifi", "wifi_name", "common")
PWD = cfg.getstr("Wifi", "wifi_password", "common")
dicttest_times = cfg.get_test_times()
test_times = 0
suc_times = 0
for TestTime in dicttest_times: test_times += int(dicttest_times[TestTime])
logger.info("Trace Total Times " + str(test_times))

# Wifi = u'Wi\u2011Fi'
Wifi = 'Wi-Fi'


def switch_wifi(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Switch Wifi %s Times." % times)
        for loop in range(times):
            try:
                logger.debug("Wifi switch Time " + str(loop + 1))
                if d1_set.stayInSetting(Wifi) and d1_set.wifi_switch():
                    suc_times += 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    d1_set.save_fail_img()
            except Exception:
                d1_set.save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug("Wifi Switch Test Complete")


def conect_wifi(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Dis/Connect Wifi %s Times." % times)
        if d1_set.stayInSetting("Wi-Fi") and d1_set.wifi_open() and d1_set.forget_all_password(SSID):
            for loop in range(times):
                try:
                    logger.debug("Wifi connect and disconnect " + str(loop + 1) + " Times")
                    if d1_set.connect_wifi(SSID, PWD) and d1_set.forget_hotspot(SSID):
                        suc_times += 1
                        logger.info("Trace Success Loop " + str(loop + 1))
                    else:
                        d1_set.save_fail_img()
                        d1_set.stayInSetting("Wi-Fi")
                        d1_set.forget_all_password(SSID)
                except Exception, e:
                    d1_set.save_fail_img()
                    common.common.log_traceback(traceback.format_exc())
                    d1_set.stayInSetting(Wifi)
                mdevice.delay(20)
        logger.debug("Wifi Connect And Disconnect Test Complete")


def reconect_wifi(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Reconnect Wifi %s Times." % times)
        for loop in range(times):
            try:
                logger.debug("Wifi reconnect Time " + str(loop + 1))
                if d1_set.set_wifi_connect("MDEVICE", SSID, PWD) and d1_set.wifi_reconnect():
                    suc_times += 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    d1_set.save_fail_img()
            except:
                d1_set.save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug("Wifi reconnect test Complete")


def switch_BT(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug("Switch BT %s Times." % times)
        for loop in range(times):
            try:
                logger.debug("BT switch Time " + str(loop + 1))
                if d1_set.stayInSetting('Bluetooth') and d1_set.BT_switch():
                    suc_times += 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    d1_set.save_fail_img()
            except Exception:
                d1_set.save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug("BY Switch Test Complete")


def main():
    logger.debug("Start Wifi Test")

    switch_wifi('SwitchWiFi')
    #     conect_wifi('ConnectTimes')
    reconect_wifi('ReconnectWiFi')
    switch_BT('SwitchBT')

    if NetworkType.find('WiFi') > -1:
        logger.debug("Open Wi-Fi after test")
        d1_set.stayInSetting("Wi-Fi") and d1_set.wifi_open() and d1_set.connect_wifi(SSID, PWD)
    else:
        logger.debug("Close Wi-Fi after test")
        d1_set.stayInSetting("Wi-Fi") and d1_set.wifi_close()

    logger.debug("Finished Wifi Test")
    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
    #  Scrpit End
