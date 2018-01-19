# -*- coding: UTF-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from infoRead import readFile
from writeLog import MwriteLog,McreateLog
from xlReadInfo import xlUserInfo

url = "http://www.maiziedu.com"
login_text = '登录'
account = 'maizi_test@139.com'
pwd = 'abc123456'

def get_ele_times(driver,times,func):
    return WebDriverWait(driver,times).until(func)

def Open_Broswer():
    '''open browser'''
    driver = webdriver.Firefox()
    return driver

def Open_Url(driver,url):
    driver.get(url)
    driver.maximize_window()


def Login_Url():
    driver = Open_Broswer()
    Open_Url(driver,url)

    ele_dict = {'url':'http://www.maiziedu.com',\
                'test_id':login_text,'userid':'account_l',\
                'pwdid':'password_l','loginid':"//div[@class='login-box marginB10']/button[@id='login_btn']",\
                'text_id':'login-form-tips'}
    ele_tuple = Find_Element(driver,ele_dict)
    # account_dict = {'uname':account,'pwd':pwd}
    account_dict = readFile(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\LoginSite\info.text')
    sendVals(ele_tuple,account_dict)
    time.sleep(5)
    driver.quit()


def Find_Element(driver,arg):

    if "test_id" in arg:
        # elelogin = get_ele_times(driver,30,driver.find_element_by_link_text(arg['test_id']))
        driver.find_element_by_link_text(arg['test_id']).click()
        time.sleep(5)
        # elelogin.click()
    userele = driver.find_element_by_name(arg['userid'])
    pawdele = driver.find_element_by_name(arg['pwdid'])
    buttonele = driver.find_element_by_xpath(arg['loginid'])
    return userele,pawdele,buttonele


def sendVals(ele_tuple,arg):
    listkey = ['account','pwd']
    i = 0
    for key in listkey:
        ele_tuple[i].send_keys('')
        ele_tuple[i].clear()
        ele_tuple[i].send_keys(arg[key])
        i += 1
    ele_tuple[2].click()



def check_Result(driver,text_id,arg,log):
    time.sleep(2)
    flag = False
    try:
        err = driver.find_element_by_id(text_id)
        # msg = "%s %s:error:%s\n"%(arg['account'],arg['pwd'],err.text)
        # writeL.MwriteInfo(msg)
        log.log_Write(arg['account'],arg['pwd'],'Error',err.text)

    except:
        # msg = "%s %s:pass\n" % (arg['account'], arg['pwd'])
        log.log_Write(arg['account'], arg['pwd'], 'pass', 'good')
        flag = True
    return flag

def Login_Out(driver):
    time.sleep(2)
    driver.find_element_by_xpath("//span[@class='nick_name']/a[@class='sign_out']").click()
    print("ok")

def Login_test(ele_dict, account_dict):
    '''开始测试'''
    d = Open_Broswer()
    Open_Url(d, ele_dict['url'])
    ele_tuple = Find_Element(d,ele_dict)
    # writeL = MwriteLog()
    log = McreateLog()
    log.log_init('sheet1', 'account', 'pwd', 'result', 'info')
    for arg in account_dict:
        sendVals(ele_tuple, arg)
        result = check_Result(d, ele_dict['text_id'],arg,log)
        if result:
            Login_Out(d)
            ele_tuple = Find_Element(d, ele_dict)
    log.log_close()
    d.quit()


if __name__ == '__main__':
    ele_dict = {'url': 'http://www.maiziedu.com', \
                'test_id': login_text, 'userid': 'account_l', \
                'pwdid': 'password_l', 'loginid': "//div[@class='login-box marginB10']/button[@id='login_btn']", \
                'text_id': 'login-form-tips'}
    # account_dict = readFile(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\LoginSite\info.text')
    #--------------调用xlReadInfo模块读取账户密码信息，文件为xlsx才能正常读取
    xinfo = xlUserInfo(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\LoginSite\info.xlsx')
    account_dict = xinfo.get_sheetinfo_by_index(0)
    Login_test(ele_dict,account_dict)
