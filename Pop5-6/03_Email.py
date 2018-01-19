#*****************************************************************************
# Title:        03_Email
#******************************************************************************
from __future__ import division
import random
import os
import traceback
import common.common
from common.getconfigs import GetConfigs
import common.settings
import common.email_tct
logger = common.common.createlogger("MAIN") 
suc_times = 0
cfg = GetConfigs("03_email")
address = cfg.getstr("Email","address","common")
RECEIVERLIST = address.split(",")

logger.debug("Connect devices")
NetworkType = cfg.getstr("Default","NETWORK_TYPE","common")
logger.info("Network Type is " + NetworkType)
mdevice= common.common.connect_device("MDEVICE") 
m_mail = common.email_tct.Email(mdevice, "M_EMAIL")
m_settings = common.settings.Settings(mdevice,'M_SETTINGS')

dicttest_times = cfg.get_test_times()
test_times = 0
suc_times = 0
NetworkType_split = NetworkType.split('/')
lenght = len(NetworkType_split)
for TestTime in dicttest_times: 
    for i in range(lenght):   
        if TestTime.upper().find(NetworkType_split[i].upper()) > -1:
            test_times += int(dicttest_times[TestTime])*2
    if TestTime.find('opentimes') > -1:
        test_times += int(dicttest_times[TestTime])*2
logger.info("Trace Total Times " + str(test_times))
    
def send_email(key,index,network_type):
    global suc_times
    times = int(dicttest_times.get(key.lower(),0))
    switch = True
    if times:
        logger.debug("Send with %d attachemnt by %s %d Times" % (index, network_type, times))
        if not key.find('WiFi') > -1:
            switch = m_settings.switch_network(network_type, os.environ.get("MDEVICE"))
        for loop in range (times):
            try:
                logger.debug('Forward email time %s', str(loop+1))
                if switch and m_mail.stay_in_email() and m_mail.enter_mailbox("Inbox") and  m_mail.forward_email(index+1,random.choice(RECEIVERLIST)):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop "+ str(loop + 1))
                    delete_box('Sent')
                    delete_box('Trash')
                else:
                    m_mail.save_fail_img()
                    delete_box("Outbox")
                    delete_box('Trash')
            except Exception,e:
                m_mail.save_fail_img()
                common.common.log_traceback(traceback.format_exc())

def open_email(key, index):
    global suc_times
    times = int(dicttest_times.get(key.lower(),0))
    if times:
        logger.info('Open Email '+str(times)+' Times')  
        for loop in range (times):
            logger.debug('Open Email time %s', str(loop+1))    
            try:
                if m_mail.stay_in_email() and m_mail.enter_mailbox("Inbox") and m_mail.select_mail(index+1):
                    suc_times = suc_times + 1
                    logger.info("Trace Success Loop "+ str(loop + 1))
                else:
                    logger.debug('Open Email time %s fail.', str(loop+1))
                    m_mail.save_fail_img()
            except Exception,e:
                m_mail.save_fail_img()
                common.common.log_traceback(traceback.format_exc())
                    
def delete_box(box):
    if m_mail.delete_mail(box):
        logger.debug('Delete %s Success', box)
    else:
        logger.warning("Delete %s Email Failed", box)
        m_mail.save_fail_img()
                    
def main():

    logger.debug('Email Start Test')
    if NetworkType.find('WiFi') > -1:
        SSID = cfg.getstr("Wifi","wifi_name","common")
        PWD = cfg.getstr("Wifi","wifi_password","common")
     
    if m_mail.if_wifi_connected(os.environ.get("MDEVICE")) or m_mail.if_data_connected(os.environ.get("MDEVICE")):
        if m_mail.stay_in_email():
            delete_box('Sent')
            delete_box('Trash')
          
    if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
#     if NetworkType.find('WiFi') > -1 :
        send_email('SendByWiFi',0,'WiFi')
    if NetworkType.find('2G') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendBy2G',0,'2G')
    if NetworkType.find('3G') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendBy3G',0,'3G')
    if NetworkType.find('LTE') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendByLTE',0,'LTE')
    if NetworkType.find('All') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendByAll',0,'All')
           
    if NetworkType.find('WiFi') > -1 and m_settings.set_wifi_connect("MDEVICE", SSID, PWD):
#     if NetworkType.find('WiFi') > -1 :
        send_email('SendByWiFi',1,'WiFi')
    if NetworkType.find('2G') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendBy2G',1,'2G')
    if NetworkType.find('3G') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendBy3G',1,'3G')
    if NetworkType.find('LTE') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendByLTE',1,'LTE')
    if NetworkType.find('All') > -1 and m_settings.set_wifi_close("MDEVICE"):
        send_email('SendByAll',1,'All')
 
#     send_email('SendBy3G',0,'3G')
#     send_email('SendByLTE',1,'LTE')
    
    if m_mail.if_wifi_connected(os.environ.get("MDEVICE")) or m_mail.if_data_connected(os.environ.get("MDEVICE")):
        open_email('opentimes', 0)
        open_email('opentimes', 1)
 
    logger.debug("Email Mission Complete")
     
    logger.info("Success Times: %s." % suc_times)
    Rate = suc_times/test_times*100
    if Rate < 95 :
        logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
    else:
        logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

if __name__ == "__main__":
    main()
# Scrpit End
