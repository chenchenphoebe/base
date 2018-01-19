# -*- coding: UTF-8 -*-
# *****************************************************************************
# Title:        08_Menu Navigation
# *****************************************************************************
from __future__ import division
from uiautomator import Device
import traceback
import common.common
import common.navigation_M

logger = common.common.createlogger("MAIN")
logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
m_nav = common.navigation_M.Navigation(mdevice, "M_MAV")


def main():
    mdevice.watcher("ALLOW").when(text="ALLOW").click(text="ALLOW")
    mdevice.watcher("GOT IT").when(text="GOT IT").click(text="GOT IT")
    FailTimes = 0
    SucTimes = 0
    logger.debug("Start Menu Navigation Test")

    mdevice.press.home()
    mdevice.press.home()

    logger.debug("Open apps in bottom")
    SucTimes, FailTimes = m_nav.click_bottom_apps(True, SucTimes, FailTimes)

    for i in range(m_nav.get_pages_count()):
        logger.debug("Go go page " + str(i + 1))
        if not m_nav.goto_page(i + 1):
            m_nav.save_fail_img()
            logger.debug("Go go next page fail.")
            break
        if i == 0 and not m_nav.is_round_pages():
            #             if m_nav.get_current_packagename() == 'com.tcl.mie.launcher.lscreen':
            if mdevice(packageName='com.tcl.mie.launcher.lscreen').exists:
                SucTimes += 1
                logger.debug("Trace Success Loop %s", SucTimes)
                m_nav.exit_app(i + 1)
            else:
                logger.debug("Can't drag left to settings")
                FailTimes += 1
                m_nav.save_fail_img()
        else:
            logger.debug("Click icons in page " + str(i + 1))
            SucTimes, FailTimes = m_nav.click_icon(i, SucTimes, FailTimes)

    if not m_nav.remove_recent_apps():
        m_nav.save_fail_img()
    mdevice.press.home()

    logger.info('Trace Total Times ' + str(SucTimes + FailTimes))

    logger.debug("Finished Menu_Navigation Test")

    if SucTimes + FailTimes <> 0:
        Rate = (SucTimes / (SucTimes + FailTimes)) * 100
    else:
        Rate = 0
    logger.info("Success Times: %s." % SucTimes)

    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
# Scrpit End
