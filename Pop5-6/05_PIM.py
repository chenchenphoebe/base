# -*- coding: UTF-8 -*-
# *****************************************************************************
# Title:        05_PIM
# *****************************************************************************
from __future__ import division
import traceback
from uiautomator import Device
import common.common
from common.calendar_google import Calendar
from common.alarm_time_tct import Alarm
from common.alarm_clock_tct import Alarm

from common.getconfigs import GetConfigs

logger = common.common.createlogger("MAIN")

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
m_cale = common.calendar_google.Calendar(mdevice, "M_CAlE")
# m_ala = common.alarm_time_tct.Alarm(mdevice, "M_ALA")
m_ala = common.alarm_clock_tct.Alarm(mdevice, "M_ALA")

test_times = 0
suc_times = 0
cfg = GetConfigs("05_pim")
dicttesttimes = cfg.get_test_times()
for test_time in dicttesttimes: test_times += int(dicttesttimes[test_time])
logger.info("Trace Total Times " + str(test_times))
calendar_task_name = []


def save_fail_img():
    m_cale.save_img("PIM")


def add_alarm(key):
    global suc_times
    times = int(dicttesttimes.get(key.lower(), 0))
    if times:
        logger.debug('Add an Alarm ' + str(times) + ' Times')
        for loop in range(times):
            try:
                if m_ala.stay_in_alarm() and m_ala.add_alarm_without_change():
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                    m_ala.discheck_alarm_current_page()
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug('Add Alarm Test complete')


def del_alarm(key):
    global suc_times
    times = int(dicttesttimes.get(key.lower(), 0))
    if times:
        logger.debug('Del an Alarm ' + str(times) + ' Times')
        for loop in range(times):
            try:
                if m_ala.stay_in_alarm() and m_ala.delete_alarm():
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop " + str(loop + 1))
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug('Delete Alarm Test complete')


def main():

    logger.debug('Start PIM Test')

    # add_calendar('AddCalendar')
    add_alarm('AddAlarm')
    # del_calendar('DelCalendar')
    del_alarm('DelAlarm')

    logger.debug('PIM Mission Complete')

    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
# Scrpit End
