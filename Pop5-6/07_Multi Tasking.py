# -*- coding: UTF-8 -*-
# *****************************************************************************
# Title:        07_Multi Tasking  
# *****************************************************************************
from __future__ import division
from uiautomator import Device
import random
import traceback
import common.common
from common.getconfigs import GetConfigs
import common.phone
import common.chrome
import common.navigation_M

logger = common.common.createlogger("MAIN")

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
m_phone = common.phone.Phone(mdevice, "M_TEL")
m_chrom = common.chrome.chrome(mdevice, "M_BROW")
m_nav = common.navigation_M.Navigation(mdevice, "M_MAV")

cfg = GetConfigs("07_multi tasking")
dicttest_times = cfg.get_test_times()
test_times = 0
suc_times = 0
for test_time in dicttest_times: test_times += int(dicttest_times[test_time])
test_times = test_times + 2
logger.info('Trace Total Times ' + str(test_times))


def save_fail_img():
    m_nav.save_img("Multi-Tasking")


def launch_apps():
    app_names = ['Messaging', 'Contacts', 'Settings', 'Camera', 'Files']

    logger.debug("Open Some apps")
    open_num = 0
    for i in range(len(app_names)):
        logger.debug("_____Open " + app_names[i])
        m_nav.enter_app(app_names[i])
        mdevice.delay(5)
        if m_nav.check_open_app(app_names[i]):
            open_num += 1
            m_nav.exit_app()
        else:
            save_fail_img()
            logger.debug("Open %s fail", app_names[i])
        logger.debug("Open %s apps successfully", str(open_num))


def call_interaction(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        try:
            logger.debug("Switch applications in call " + str(times) + " Times")
            for loop in range(times):
                if m_phone.call_from_dailerpad('10010') and interaction(4) and m_phone.end_call():
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop %s.", str(loop + 1))
                else:
                    save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())


def chrome_interaction(key):
    global suc_times
    start_chrome()
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        try:
            logger.debug("Switch applications in chrome " + str(times) + " Times")
            for loop in range(times):
                if interaction(1):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop %s.", str(loop))
                else:
                    save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())
    exit_chrome()


def interaction(times):
    global suc_times
    if times:
        logger.debug("Switch applications " + str(times) + " Times")
        for loop in range(times):
            try:
                mdevice.press.recent()
                mdevice.delay(3)
                if mdevice(text='Your recent screens appear here').exists:
                    logger.debug("There is none recent apps")
                    save_fail_img()
                    break
                elif mdevice(resourceId='com.android.systemui:id/recents_view').child(
                        resourceId='com.android.systemui:id/activity_description').exists:
                    if mdevice(resourceId='com.android.systemui:id/activity_description').count < 2:
                        logger.debug("There is on other recent app")
                        save_fail_img()
                    else:
                        max_swipe = 0
                        while mdevice(resourceId='com.android.systemui:id/activity_description').count > 3:
                            logger.debug("Swipe one time")
                            #                             mdevice.swipe(288, 150, 288, 950, steps=5)
                            mdevice(resourceId='com.android.systemui:id/recents_view').child(
                                className='android.widget.FrameLayout', instance=0).swipe.down(steps=5)
                            max_swipe += 1
                            if max_swipe > 5:
                                break
                        if max_swipe > 0:
                            mdevice.delay(4)
                        app_name = mdevice(resourceId='com.android.systemui:id/activity_description', instance=mdevice(
                            resourceId='com.android.systemui:id/activity_description').count - 1).get_text()
                        if app_name is not None and app_name is not 'Ongoing call':
                            mdevice(text=app_name).click.topleft()
                            mdevice.delay(2)
                            if m_nav.check_open_app(app_name):
                                logger.info("Open /%s successfully ", app_name)
                            else:
                                logger.debug('can not switch to recent app ' + app_name)
                                save_fail_img()
                                return False
                        else:
                            logger.debug("Get the first app name fail")
                            save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
                return False

        logger.info("Open recent app %s times successfully ", str(times))
        return True


def start_chrome():
    global suc_times
    try:
        if m_chrom.enter_chrome() and m_chrom.enter_homePage():
            suc_times = suc_times + 1
            logger.debug("Trace Success Start Browser")
        else:
            save_fail_img()
    except Exception, e:
        save_fail_img()
        common.common.log_traceback(traceback.format_exc())


def exit_chrome():
    global suc_times
    try:
        if m_nav.exit_app(1):
            suc_times = suc_times + 1
            logger.debug("Trace Success exit Chrome")
        else:
            save_fail_img()
            logger.debug("Exit Browser failed")
    except Exception, e:
        save_fail_img()
        common.common.log_traceback(traceback.format_exc())


def main():
    global suc_times
    logger.debug('Start Multi tasking Test')

    m_nav.remove_recent_apps()
    launch_apps()

    call_interaction('IteractionsCall')
    chrome_interaction('Iteractionschrome')

    logger.debug("Finished Multi-Tasking Test")

    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
# Scrpit End
