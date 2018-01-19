# -*- coding: UTF-8 -*-
# *****************************************************************************
# Title:        01_Telephony
# *****************************************************************************

from __future__ import division
from uiautomator import Device
import traceback
import os
import common.common
from common.getconfigs import GetConfigs
import common.phone
import common.contact
import common.settings

logger = common.common.createlogger("MAIN")

logger.debug("Connect devices")
mdevice = common.common.connect_device("MDEVICE")
m_phone = common.phone.Phone(mdevice, "M_TEL")
m_contacts = common.contact.Contact(mdevice, "M_CONTACT")
m_settings = common.settings.Settings(mdevice, "M_SETTINGS")

cfg = GetConfigs("01_telephony")
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
    if (TestTime.upper() == 'DelContactsTimes'.upper()) or (TestTime.upper() == 'AddContactsTimes'.upper()) or (
        TestTime.upper() == 'CallformContactsTimes'.upper()) or (TestTime.upper() == 'CallformCallLogTimes'.upper()):
        test_times += int(dicttest_times[TestTime])
logger.info("Trace Total Times " + str(test_times))


def save_fail_img():
    m_contacts.save_img("Telephony")


def call_from_contact(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug('call from contact ' + str(times) + ' Times')
        try:
            if m_contacts.stay_in_contact('Contacts') and m_contacts.delete_all_contacts(
                    'Contacts') and m_contacts.import_contacts('Contacts'):
                for loop in range(times):
                    logger.debug(" Call from Contact " + str(loop + 1) + ' Times')
                    if m_contacts.stay_in_contact('Contacts') and m_contacts.call_from_contacts(
                                    'Autotest' + str(loop + 1 + 50).zfill(6)):
                        suc_times = suc_times + 1
                        logger.info("Trace Success Loop %s." % (loop + 1))
                    else:
                        save_fail_img()
        except Exception, e:
            save_fail_img()
            common.common.log_traceback(traceback.format_exc())
        logger.debug(" Call From Contacts Test complete")


def call_from_callLog(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    switch = True
    if times:
        logger.debug("Test Call from CallLog %s Times", times)
        for loop in range(times):
            try:
                logger.debug(" Call from Calllog " + str(loop + 1) + " time")
                if switch and m_phone.call_from_callLog('Recent'):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop %s." % (loop + 1))
                else:
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())
        logger.debug(" Call From Calllog Test complete")


def delete_contact(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug('Delete a contact from the Contacts ' + str(times) + ' Times')
        if m_contacts.stay_in_contact('Contacts'):
            for loop in range(times):
                try:
                    if m_contacts.import_contacts('Contacts') and m_contacts.delete_all_contacts('Contacts'):
                        suc_times = suc_times + 1
                        logger.info("Trace Success Loop %s." % (loop + 1))
                    else:
                        logger.warning("Cannot delete contact")
                        save_fail_img()
                except Exception, e:
                    save_fail_img()
                    common.common.log_traceback(traceback.format_exc())
            logger.debug(" Delete Contact Test complete")


def add_contact(key):
    global suc_times
    times = int(dicttest_times.get(key.lower(), 0))
    if times:
        logger.debug('Add a contact ' + str(times) + ' Times')

        for loop in range(0, times):
            try:
                if m_contacts.stay_in_contact('Contacts') and m_contacts.add_a_contact(
                                'Autotest' + str(loop + 1).zfill(6), m_contacts.random_number(10), True):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop %s." % (loop + 1))
                else:
                    logger.warning("Add a contact fail.")
                    save_fail_img()
            except Exception, e:
                save_fail_img()
                common.common.log_traceback(traceback.format_exc())


def main():
    logger.debug('Start Telephony Test')
    add_contact('AddContactsTimes')
    call_from_contact('CallformContactsTimes')
    call_from_callLog('CallformCallLogTimes')
    delete_contact('DelContactsTimes')

    logger.debug("Telephony Mission Complete")
    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times / test_times * 100
    if Rate < 95:
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')


if __name__ == "__main__":
    main()
