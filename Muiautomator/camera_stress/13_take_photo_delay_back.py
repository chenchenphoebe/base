# -*- coding: UTF-8 -*-
# *****************************************************************************
# Title:
#             1.test camera delay for back
# Precondition:
#             1.NA
# Procedure:
#             1.open the camera delay for back and cycle 10 times
#             2.check the camera number
# Expectation:
#             1.take photo successfully
# Platform:     7.0
# Project:      Pop5-6 4G
# author:       bei.han
# *****************************************************************************
from __future__ import division

import traceback
import unittest
import os

from uiautomator import Device

import common.common
from common.getconfigs import GetConfigs
from common.camera_stress import Camera

logger = common.common.createlogger("MAIN")
logger.debug("Connect device")
mdevice = common.common.connect_device("MDEVICE")
m_com = common.common.Common(mdevice, "M_COMMON")
m_camera = common.camera_stress.Camera(mdevice, "m_camera")
logger.debug('Get some configrations')
cfg = GetConfigs('13_camera_delay_back')
dicttest_times = cfg.get_test_times()
test_times = 0
suc_times = 0
for TestTime in dicttest_times: test_times += int(dicttest_times[TestTime])
logger.info("Trace Total Times " + str(test_times))


class CheckCamera(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        m_com.registerWatchers()
        m_com.clear_recent()
        logger.info("------------------Start check camera delay for back")

    @classmethod
    def tearDownClass(cls):
        m_com.removeWatchers()
        mdevice.press.back()
        logger.info("Success Times: %s." % suc_times)
        Rate = suc_times / test_times * 100

        if Rate < 100:
            logger.warning("-------------------Result Fail Success Rate Is " + str(Rate) + '%')

        else:
            logger.info("--------------------Result Pass Success Rate Is " + str(Rate) + '%')


    def testCameradelayBack(self):
        global suc_times
        times = int(dicttest_times.get('camera_delay_back'.lower(), 0))
        if times:
            logger.debug("start camera delay for back test")
            if m_camera.stay_in_camera() and m_camera.switch_back_front("back"):
                for loop in range(times):
                    try:
                        logger.debug('test camera delay for back ' + str(loop + 1) + ' Times')
                        if m_camera.switch_delay_mode():
                            suc_times += 1
                            logger.debug('Trace success loop ' + str(loop + 1))
                        else:
                            m_camera.save_fail_img()
                    except Exception:
                        m_camera.save_fail_img()
                        common.common.log_traceback(traceback.format_exc())
            else:
                m_camera.save_fail_img()
            m_com.clear_recent()
            if m_camera.gallery_pic_del():
                logger.debug("delete the all pirture successfully")
            else:
                m_camera.save_fail_img()
            logger.debug("----------------------test camera delay for back completely")


if __name__ == "__main__":
    common.common.runTest(CheckCamera, [
        "testCameradelayBack",
    ])
